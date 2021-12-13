output "ecr_repository_endpoint" {
  value = aws_ecr_repository.mp_app.repository_url
}

output "iam_role_name" {
  value = aws_iam_role.mp_app_ecs_agent.name
}
