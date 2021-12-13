output "subnet_id" {
  value = aws_subnet.mp_public_subnet.id
}

output "security_group_id" {
  value = aws_security_group.mp_app_ecs_sg.id
}

output "security_group_name" {
  value = aws_security_group.mp_app_ecs_sg.name
}