output "mysql_address" {
  value = module.mysql.address
}

output "ecr_repo_url" {
  value = module.core.ecr_repository_endpoint
}