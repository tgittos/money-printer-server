variable "ecs_security_group_id" {
  description = "The ID of the ECS security group to assign to instances in this cluster"
  type = string
}

variable "db_security_group_id" {
  description = "The ID of the DB security group to assign to instances in this cluster"
  type = string
}

variable "subnet_group_id" {
  description = "The ID of the subnet group into which to put instances in this cluster"
  type = string
}
