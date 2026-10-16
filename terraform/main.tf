# main.tf – top-level locals and data sources

locals {
  name_prefix = "taskboard-${var.environment}"
}

# Convenience: current AWS region
data "aws_region" "current" {}
