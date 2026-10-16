provider "aws" {
  region = var.aws_region

  # AWS credentials are read from environment variables or ~/.aws/credentials.
  # NEVER hardcode credentials here.
  # Recommended: use AWS SSO or assume an IAM role.

  default_tags {
    tags = {
      Project     = "TaskBoard"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
    }
  }
}

# Kubernetes provider – configured after EKS cluster is created.
# The data source reads cluster details from AWS.
data "aws_eks_cluster_auth" "taskboard" {
  name = aws_eks_cluster.taskboard.name
}

provider "kubernetes" {
  host = aws_eks_cluster.taskboard.endpoint
  cluster_ca_certificate = base64decode(
    aws_eks_cluster.taskboard.certificate_authority[0].data
  )
  token = data.aws_eks_cluster_auth.taskboard.token
}
