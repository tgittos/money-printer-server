module "api_cluster" {
  source = "../../../modules/small-cluster"

  cluster_prefix = "api_staging"
  task_definition_filename = "${path.module}/../../task-definitions/api.json.tpl"
  ecr_repo_url = var.ecr_repo_url
  image_id = ""
  instance_type = ""
  iam_instance_profile_name = var.iam_instance_profile_name
  security_group_id = var.security_group_id
  subnet_id = var.subnet_id
}
