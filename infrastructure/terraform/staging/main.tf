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
    profile = "default"
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

module "core" {
  source = "../core"
}

module "vpc" {
  source = "../modules/vpc"
}

module "mysql" {
  source = "./storage/mysql"

  subnet_group_id = module.vpc.subnet_id
  ecs_security_group_id = module.vpc.ecs_security_group_id
  db_security_group_id = module.vpc.db_security_group_id
}

module "api" {
  source = "./services/api"

  ecr_repo_url = module.core.ecr_repository_endpoint
  iam_instance_profile_name = module.core.iam_role_name
  security_group_id = module.vpc.ecs_security_group_id
  subnet_id = module.vpc.subnet_id
}

module "ds" {
  source = "./services/data-server"

  ecr_repo_url = module.core.ecr_repository_endpoint
  iam_instance_profile_name = module.core.iam_role_name
  security_group_id = module.vpc.ecs_security_group_id
  subnet_id = module.vpc.subnet_id
}

module "tr" {
  source = "./services/task-runner"

  ecr_repo_url = module.core.ecr_repository_endpoint
  iam_instance_profile_name = module.core.iam_role_name
  security_group_id = module.vpc.ecs_security_group_id
  subnet_id = module.vpc.subnet_id
}
