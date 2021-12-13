resource "aws_db_instance" "mp_app_staging_mysql" {
  identifier                = "mp-staging-mysql"
  allocated_storage         = 5
  backup_retention_period   = 2
  backup_window             = "01:00-01:30"
  maintenance_window        = "sun:03:00-sun:03:30"
  multi_az                  = true
  engine                    = "mysql"
  engine_version            = "5.7"
  instance_class            = "db.t2.micro"
  name                      = "mp-staging-mysql"
  port                      = "3306"
  db_subnet_group_name      = var.subnet_group_id
  vpc_security_group_ids    = [var.db_security_group_id, var.ecs_security_group_id]
  skip_final_snapshot       = true
  final_snapshot_identifier = "mp-staging-mysql-final"
  publicly_accessible       = true
}
