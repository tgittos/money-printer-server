resource "aws_db_instance" "mp_app_mysql" {
  identifier                = "mp-mysql"
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
