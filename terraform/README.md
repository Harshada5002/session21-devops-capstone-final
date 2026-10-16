# Terraform Infrastructure – README

## Overview

This directory provisions the AWS infrastructure for TaskBoard:

- **VPC** with public and private subnets across 2 AZs
- **Internet Gateway** for public internet access
- **NAT Gateway** for outbound access from private subnets
- **Amazon EKS** control plane and managed node group
- **IAM roles** with least-privilege policies
- **OIDC provider** for GitHub Actions keyless authentication

## Cost Estimate (ap-south-1)

| Resource | ~Cost/Hour | ~Cost/Day |
|----------|-----------|-----------|
| EKS control plane | $0.10 | $2.40 |
| 2× t3.medium nodes | $0.05 | $1.20 |
| NAT Gateway | $0.045 | $1.08 |
| Load Balancer (if created) | $0.025 | $0.60 |
| **Total** | **~$0.22** | **~$5.28** |

> **Always run `terraform destroy` when finished to avoid ongoing charges.**

## Prerequisites

1. AWS CLI configured: `aws configure`
2. Terraform 1.9+: `winget install Hashicorp.Terraform`
3. Permissions: AdministratorAccess or equivalent custom policy

## Bootstrap Remote State (Optional but Recommended for Teams)

```powershell
# Create S3 bucket for state storage
aws s3 mb s3://your-terraform-state-bucket --region ap-south-1
aws s3api put-bucket-versioning `
  --bucket your-terraform-state-bucket `
  --versioning-configuration Status=Enabled

# Create DynamoDB table for locking
aws dynamodb create-table `
  --table-name terraform-state-lock `
  --attribute-definitions AttributeName=LockID,AttributeType=S `
  --key-schema AttributeName=LockID,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --region ap-south-1
```

Then uncomment the `backend "s3"` block in `versions.tf`.

## Workflow

```powershell
# Navigate to terraform directory
cd session21-devops-capstone-final\terraform

# Initialize providers and modules
terraform init

# Validate syntax
terraform validate

# Preview changes (ALWAYS review before applying)
terraform plan

# Apply (creates real AWS resources that cost money)
terraform apply

# Get outputs
terraform output

# Destroy ALL resources (permanent – review carefully)
terraform destroy
```

## After Apply

```powershell
# Configure kubectl
aws eks update-kubeconfig --region ap-south-1 --name taskboard-cluster

# Verify nodes
kubectl get nodes

# Install Metrics Server (required for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Replacing Variables

Edit `variables.tf` or create a `terraform.tfvars` file:

```hcl
# terraform.tfvars  ← never commit this file
aws_region         = "ap-south-1"
environment        = "dev"
node_instance_type = "t3.small"   # cheaper for learning
node_desired_size  = 1
```
