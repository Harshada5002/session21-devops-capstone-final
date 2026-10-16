output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.taskboard.id
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.taskboard.name
}

output "cluster_endpoint" {
  description = "EKS API server endpoint"
  value       = aws_eks_cluster.taskboard.endpoint
}

output "cluster_certificate_authority_data" {
  description = "Base64-encoded CA certificate"
  value       = aws_eks_cluster.taskboard.certificate_authority[0].data
  sensitive   = true
}

output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.taskboard.name}"
}

output "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC authentication"
  value       = aws_iam_role.github_actions.arn
}

output "nat_gateway_ip" {
  description = "Public IP of the NAT Gateway (add to security group allowlists if needed)"
  value       = aws_eip.nat.public_ip
}
