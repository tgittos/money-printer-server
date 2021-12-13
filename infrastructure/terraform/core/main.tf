terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  backend "s3" {
      bucket = "moneyprinter-aws"
      key    = "terraform/state.tfstate"
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

// ecr
resource "aws_ecr_repository" "mp_app" {
  name  = "mp_app"
}

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

module "vpc" {
  source = "../modules/vpc"
}

module "aws_runner_ecs" {
  source = "./services/gitlab-runner"

  ecr_repo_url = aws_ecr_repository.mp_app.repository_url
  iam_instance_profile_name = aws_iam_role.mp_app_ecs_agent.name
  security_group_id = module.vpc.ecs_security_group_id
  subnet_id = module.vpc.subnet_id
}