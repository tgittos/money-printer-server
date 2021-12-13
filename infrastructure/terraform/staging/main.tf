terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  backend "s3" {
      bucket = "moneyprinter_aws"
      key    = "terraform/staging/state.tfstate"
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

module "_cluster" {
  source = "../modules/small-cluster"

  cluster_prefix = "api_staging"
  task_definition_filename = "api.json.tpl"
  ecr_repo_url = module.core.ecr_repository_endpoint
  image_id = ""
  instance_type = ""
  iam_instance_profile_name = module.core.iam_role_name
  security_group_id = module.vpc.security_group_name
  subnet_id = module.vpc.subnet_id
}
