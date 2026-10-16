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
  name = module.eks.cluster_name
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.taskboard.token
}
