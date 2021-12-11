terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  backend "s3" {
      bucket = "moneyprinter_aws"
      key    = "platform/state.tfstate"
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

//******************************************************
//* Data template files
//******************************************************

data "template_file" "api_task_definition" {
  template = "${file("${path.module}/task_definitions/api.json.tpl")}"
  vars = {
    repository_url = aws_ecr_repository.mp_app.repository_url
  }
}

data "template_file" "ds_task_definition" {
  template = "${file("${path.module}/task_definitions/data-server.json.tpl")}"
  vars = {
    repository_url = aws_ecr_repository.mp_app.repository_url
  }
}

data "template_file" "tr_task_definition" {
  template = "${file("${path.module}/task_definitions/task-runner.json.tpl")}"
  vars = {
    repository_url = aws_ecr_repository.mp_app.repository_url
  }
}

//******************************************************
//* Networking
//******************************************************

// vpc
resource "aws_vpc" "mp_vpc" {
    cidr_block = "10.0.0.0/24"
    enable_dns_support   = true
    enable_dns_hostnames = true
    tags       = {
        Name = "MoneyPrinter VPC"
    }
}

resource "aws_internet_gateway" "internet_gateway" {
    vpc_id = aws_vpc.mp_vpc.id
}

// subnets
resource "aws_subnet" "mp_pub_subnet" {
    vpc_id                  = aws_vpc.mp_vpc.id
    cidr_block              = "10.1.0.0/22"
}

resource "aws_db_subnet_group" "mp_db_subnet_group" {
    subnet_ids  = [aws_subnet.mp_pub_subnet.id]
}

// route table
resource "aws_route_table" "mp_rt_public" {
    vpc_id = aws_vpc.mp_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.internet_gateway.id
    }
}

resource "aws_route_table_association" "route_table_association" {
    subnet_id      = aws_subnet.mp_pub_subnet.id
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

//******************************************************
//* IAM Roles and Permissions
//******************************************************

// iam role
data "aws_iam_policy_document" "mp_app_ecs_agent" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "mp_app_ecs_agent" {
  name               = "mp_app_ecs_agent"
  assume_role_policy = data.aws_iam_policy_document.mp_app_ecs_agent.json
}

resource "aws_iam_role_policy_attachment" "mp_app_ecs_agent" {
  role       = "aws_iam_role.mp_app_ecs_agent.name"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "mp_app_ecs_agent" {
  name = "ecs-mp_app_ecs_agent"
  role = aws_iam_role.mp_app_ecs_agent.name
}

//******************************************************
//* Autoscaling groups
//******************************************************

resource "aws_launch_configuration" "mp_app_ecs_launch_config" {
    image_id             = "ami-094d4d00fd7462815"
    iam_instance_profile = aws_iam_instance_profile.mp_app_ecs_agent.name
    security_groups      = [aws_security_group.mp_app_ecs_sg.id]
    user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-app-ecs-cluster >> /etc/ecs/ecs.config"
    instance_type        = "t2.micro"
}

resource "aws_launch_configuration" "mp_data_ecs_launch_config" {
    image_id             = "ami-094d4d00fd7462815"
    iam_instance_profile = aws_iam_instance_profile.mp_app_ecs_agent.name
    security_groups      = [aws_security_group.mp_app_ecs_sg.id]
    user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-data-ecs-cluster >> /etc/ecs/ecs.config"
    instance_type        = "t2.micro"
}

resource "aws_launch_configuration" "mp_worker_ecs_launch_config" {
    image_id             = "ami-094d4d00fd7462815"
    iam_instance_profile = aws_iam_instance_profile.mp_app_ecs_agent.name
    security_groups      = [aws_security_group.mp_app_ecs_sg.id]
    user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-worker-ecs-cluster >> /etc/ecs/ecs.config"
    instance_type        = "t2.micro"
}

resource "aws_autoscaling_group" "mp_app_ecs_asg" {
    name                      = "mp-app-asg"
    vpc_zone_identifier       = [aws_subnet.mp_pub_subnet.id]
    launch_configuration      = aws_launch_configuration.mp_app_ecs_launch_config.name

    desired_capacity          = 1
    min_size                  = 1
    max_size                  = 2
    health_check_grace_period = 300
    health_check_type         = "EC2"
}

resource "aws_autoscaling_group" "mp_data_ecs_asg" {
    name                      = "mp-data-asg"
    vpc_zone_identifier       = [aws_subnet.mp_pub_subnet.id]
    launch_configuration      = aws_launch_configuration.mp_data_ecs_launch_config.name

    desired_capacity          = 1
    min_size                  = 1
    max_size                  = 10
    health_check_grace_period = 300
    health_check_type         = "EC2"
}

resource "aws_autoscaling_group" "mp_worker_ecs_asg" {
    name                      = "mp-worker-asg"
    vpc_zone_identifier       = [aws_subnet.mp_pub_subnet.id]
    launch_configuration      = aws_launch_configuration.mp_worker_ecs_launch_config.name

    desired_capacity          = 1
    min_size                  = 1
    max_size                  = 10
    health_check_grace_period = 300
    health_check_type         = "EC2"
}


//******************************************************
//* Database
//******************************************************

resource "aws_db_instance" "mp_app_mysql" {
    identifier                = "mysql"
    allocated_storage         = 5
    backup_retention_period   = 2
    backup_window             = "01:00-01:30"
    maintenance_window        = "sun:03:00-sun:03:30"
    multi_az                  = true
    engine                    = "mysql"
    engine_version            = "5.7"
    instance_class            = "db.t2.micro"
    name                      = "worker_db"
    username                  = "worker"
    password                  = "worker"
    port                      = "3306"
    db_subnet_group_name      = aws_db_subnet_group.mp_db_subnet_group.id
    vpc_security_group_ids    = [aws_security_group.mp_app_rds_sg.id, aws_security_group.mp_app_ecs_sg.id]
    skip_final_snapshot       = true
    final_snapshot_identifier = "worker-final"
    publicly_accessible       = true
}

//******************************************************
//* ECR
//******************************************************

resource "aws_ecr_repository" "mp_app" {
    name  = "mp_app"
}

//******************************************************
//* ECS clusters
//******************************************************
resource "aws_ecs_cluster" "mp_app_ecs_cluster" {
    name  = "mp-app-ecs-cluster"
}

resource "aws_ecs_cluster" "mp_data_ecs_cluster" {
    name  = "mp-data-ecs-cluster"
}

resource "aws_ecs_cluster" "mp_worker_ecs_cluster" {
  name  = "mp-worker-ecs-cluster"
}

//******************************************************
//* ECS task definition
//******************************************************

resource "aws_ecs_task_definition" "mp_app_task_definition" {
  family                = "app"
  container_definitions = data.template_file.api_task_definition.rendered
}

resource "aws_ecs_task_definition" "mp_ds_task_definition" {
  family                = "data_server"
  container_definitions = data.template_file.ds_task_definition.rendered
}

resource "aws_ecs_task_definition" "mp_tr_task_definition" {
  family                = "task_runner"
  container_definitions = data.template_file.tr_task_definition.rendered
}

//******************************************************
//* ECS services
//******************************************************

resource "aws_ecs_service" "mp_app_api_ecs_service" {
  name            = "api"
  cluster         = aws_ecs_cluster.mp_app_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_app_task_definition.arn
  desired_count   = 1
}

resource "aws_ecs_service" "mp_app_ds_ecs_service" {
  name            = "data-server"
  cluster         = aws_ecs_cluster.mp_data_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_ds_task_definition.arn
  desired_count   = 1
}

resource "aws_ecs_service" "mp_app_tr_ecs_service" {
  name            = "task-runner"
  cluster         = aws_ecs_cluster.mp_worker_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_tr_task_definition.arn
  desired_count   = 1
}

//******************************************************
//* Outputs
//******************************************************

output "mysql_endpoint" {
    value = aws_db_instance.mp_app_mysql.endpoint
}

output "ecr_repository_app_endpoint" {
    value = aws_ecr_repository.mp_app.repository_url
}
