output "subnet_id" {
  value = aws_subnet.mp_public_subnet.id
}

output "ecs_security_group_id" {
  value = aws_security_group.mp_app_ecs_sg.id
}

output "ecs_security_group_name" {
  value = aws_security_group.mp_app_ecs_sg.name
}

output "db_security_group_id" {
  value = aws_security_group.mp_app_rds_sg.id
}