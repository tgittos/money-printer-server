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

//******************************************************
//* Networking
//******************************************************

//******************************************************
//* IAM Roles and Permissions
//******************************************************

//******************************************************
//* Autoscaling groups
//******************************************************


//******************************************************
//* Database
//******************************************************

//******************************************************
//* ECR
//******************************************************

//******************************************************
//* ECS clusters
//******************************************************

//******************************************************
//* ECS task definition
//******************************************************

//******************************************************
//* ECS services
//******************************************************

//******************************************************
//* Outputs
//******************************************************

output "mysql_endpoint" {
    value = aws_db_instance.mp_app_mysql.endpoint
}

output "ecr_repository_app_endpoint" {
    value = aws_ecr_repository.mp_app.repository_url
}
