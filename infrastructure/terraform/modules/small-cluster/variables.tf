variable "cluster_prefix" {
  description = "The name of the cluster eg: api, worker, ds"
  type = string
}

variable "task_definition_filename" {
  description = "The filename the the JSON task definition for this cluster"
  type = string
}

variable "ecr_repo_url" {
  description = "The url for the platform's ECR repository (used to push/pull images from builds to envs)"
  type = string
}

variable "image_id" {
  description = "The image ID of the Docker image to deploy to instances"
  type = string
}

variable "instance_type" {
  description = "The type of the AWS EC2 instance to deploy into the cluster"
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
