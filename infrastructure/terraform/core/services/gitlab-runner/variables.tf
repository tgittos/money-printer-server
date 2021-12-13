variable "ecr_repo_url" {
  description = "The url for the platform's ECR repository (used to push/pull images from builds to envs)"
  type = string
}

variable "iam_instance_profile_name" {
  description = "The name of the IAM profile that owns instances in this cluster"
  type = string
}

variable "security_group_id" {
  description = "The ID of the security group to assign to instances in this cluster"
  type = string
}

variable "subnet_id" {
  description = "The ID of the subnet into which to put instances in this cluster"
  type = string
}
