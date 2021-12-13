resource "aws_vpc" "mp_vpc" {
  cidr_block = "10.0.0.0/24"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "mp_ig" {
  vpc_id = aws_vpc.mp_vpc.id
}

// subnets
resource "aws_subnet" "mp_public_subnet" {
  vpc_id                  = aws_vpc.mp_vpc.id
  cidr_block              = "10.1.0.0/22"
}

resource "aws_db_subnet_group" "mp_db_subnet_group" {
  subnet_ids  = [aws_subnet.mp_public_subnet.id]
}

// route table
resource "aws_route_table" "mp_rt_public" {
  vpc_id = aws_vpc.mp_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mp_ig.id
  }
}

resource "aws_route_table_association" "mp_rta" {
  subnet_id      = aws_subnet.mp_public_subnet.id
  route_table_id = aws_route_table.mp_rt_public.id
}

// security groups - one for app servers, one for db servers
resource "aws_security_group" "mp_app_ecs_sg" {
  vpc_id      = aws_vpc.mp_vpc.id

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "mp_app_rds_sg" {
  vpc_id      = aws_vpc.mp_vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = 3306
    to_port         = 3306
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.mp_app_ecs_sg.id]
  }

  egress {
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}
