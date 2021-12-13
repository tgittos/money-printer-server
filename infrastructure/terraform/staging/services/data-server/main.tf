module "api_cluster" {
  source = "../../../modules/small-cluster"

  cluster_prefix = "ds_staging"
  task_definition_filename = "data-server.json.tpl"
  ecr_repo_url = var.ecr_repo_url
  image_id = ""
  instance_type = ""
  iam_instance_profile_name = var.iam_instance_profile_name
  security_group_id = var.security_group_id
  subnet_id = var.subnet_id
}
