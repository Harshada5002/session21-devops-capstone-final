# ── VPC ───────────────────────────────────────────────────────────────────────
resource "aws_vpc" "taskboard" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true    # required for EKS node-to-control-plane communication

  tags = { Name = "taskboard-vpc-${var.environment}" }
}

# ── Internet Gateway ───────────────────────────────────────────────────────────
resource "aws_internet_gateway" "taskboard" {
  vpc_id = aws_vpc.taskboard.id
  tags   = { Name = "taskboard-igw-${var.environment}" }
}

# ── Public Subnets ─────────────────────────────────────────────────────────────
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.taskboard.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  # Instances launched here get a public IP automatically.
  # Required for load balancers and NAT gateways.
  map_public_ip_on_launch = true

  tags = {
    Name                                        = "taskboard-public-${count.index + 1}-${var.environment}"
    # These tags allow the AWS Load Balancer Controller to discover subnets.
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }
}

# ── Private Subnets ────────────────────────────────────────────────────────────
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.taskboard.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name                                        = "taskboard-private-${count.index + 1}-${var.environment}"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

# ── Elastic IP for NAT Gateway ─────────────────────────────────────────────────
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = { Name = "taskboard-nat-eip-${var.environment}" }
}

# ── NAT Gateway ────────────────────────────────────────────────────────────────
# Private subnet nodes use this to reach the internet (pulling images, etc.)
# without having public IP addresses.
# COST NOTE: NAT Gateway charges ~$0.045/hour + data transfer fees in ap-south-1.
# Destroy when not in use to avoid ongoing costs.
resource "aws_nat_gateway" "taskboard" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id   # NAT GW sits in the first public subnet
  depends_on    = [aws_internet_gateway.taskboard]
  tags          = { Name = "taskboard-nat-${var.environment}" }
}

# ── Route Tables ───────────────────────────────────────────────────────────────

# Public route table: routes all traffic through the Internet Gateway
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.taskboard.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.taskboard.id
  }
  tags = { Name = "taskboard-public-rt-${var.environment}" }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private route table: routes internet traffic through the NAT Gateway
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.taskboard.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.taskboard.id
  }
  tags = { Name = "taskboard-private-rt-${var.environment}" }
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
