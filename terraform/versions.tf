terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.73"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.33"
    }
  }

  # ── Remote state (S3 + DynamoDB locking) ─────────────────────────────────
  # Uncomment and configure AFTER creating the S3 bucket and DynamoDB table.
  # See terraform/README.md for bootstrap instructions.
  #
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "taskboard/terraform.tfstate"
  #   region         = "ap-south-1"
  #   dynamodb_table = "terraform-state-lock"
  #   encrypt        = true
  # }
}
