module "rds" {
  source = "../../../modules/rds"

  subnet_group_id = var.subnet_group_id
  ecs_security_group_id = var.ecs_security_group_id
  db_security_group_id = var.db_security_group_id
}