# ── EKS Cluster IAM Role ───────────────────────────────────────────────────────
data "aws_iam_policy_document" "eks_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eks_cluster" {
  name               = "taskboard-eks-cluster-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.eks_assume_role.json
  tags               = { Name = "taskboard-eks-cluster-role" }
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

# ── Node Group IAM Role ────────────────────────────────────────────────────────
data "aws_iam_policy_document" "node_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eks_node_group" {
  name               = "taskboard-eks-node-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.node_assume_role.json
  tags               = { Name = "taskboard-eks-node-role" }
}

resource "aws_iam_role_policy_attachment" "worker_node" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_group.name
}

resource "aws_iam_role_policy_attachment" "cni" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_group.name
}

resource "aws_iam_role_policy_attachment" "ecr_read" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_group.name
}

# ── EKS Cluster ───────────────────────────────────────────────────────────────
resource "aws_eks_cluster" "taskboard" {
  name     = var.cluster_name
  version  = var.cluster_version
  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    subnet_ids              = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
    endpoint_public_access  = true
    endpoint_private_access = true
    # For production: restrict public_access_cidrs to your office/VPN IP range.
    # public_access_cidrs = ["YOUR_IP/32"]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator"]

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_internet_gateway.taskboard,
  ]

  tags = { Name = "taskboard-eks-${var.environment}" }
}

# ── Managed Node Group ─────────────────────────────────────────────────────────
resource "aws_eks_node_group" "taskboard" {
  cluster_name    = aws_eks_cluster.taskboard.name
  node_group_name = "taskboard-nodes-${var.environment}"
  node_role_arn   = aws_iam_role.eks_node_group.arn
  subnet_ids      = aws_subnet.private[*].id # nodes in private subnets

  instance_types = [var.node_instance_type]

  scaling_config {
    desired_size = var.node_desired_size
    min_size     = var.node_min_size
    max_size     = var.node_max_size
  }

  update_config {
    max_unavailable = 1 # rolling update: at most 1 node unavailable at a time
  }

  # Use Amazon Linux 2023 (AL2023) for improved security and performance
  ami_type      = "AL2023_x86_64_STANDARD"
  capacity_type = "ON_DEMAND"
  disk_size     = 20 # GB – increase if storing large container images

  depends_on = [
    aws_iam_role_policy_attachment.worker_node,
    aws_iam_role_policy_attachment.cni,
    aws_iam_role_policy_attachment.ecr_read,
  ]

  tags = { Name = "taskboard-node-${var.environment}" }

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}

# ── OIDC Provider (for GitHub Actions and IRSA) ───────────────────────────────
data "tls_certificate" "eks" {
  url = aws_eks_cluster.taskboard.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.taskboard.identity[0].oidc[0].issuer
}

# ── GitHub Actions IAM Role (OIDC-based, no long-lived keys) ──────────────────
# Replace GITHUB_ORG and GITHUB_REPO with your actual values before applying.
locals {
  github_org  = "REPLACE_WITH_YOUR_GITHUB_ORG"
  github_repo = "REPLACE_WITH_YOUR_GITHUB_REPO"
}

data "aws_iam_policy_document" "github_actions_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${local.github_org}/${local.github_repo}:*"]
    }
  }
}

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "github_actions" {
  name               = "TaskBoardGitHubActionsRole"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume.json
  tags               = { Name = "taskboard-github-actions-role" }
}

resource "aws_iam_role_policy" "github_actions_eks" {
  name = "taskboard-eks-deploy"
  role = aws_iam_role.github_actions.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["eks:DescribeCluster"]
      Resource = aws_eks_cluster.taskboard.arn
    }]
  })
}
