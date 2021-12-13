data "template_file" "api_task_definition" {
  template = file(var.task_definition_filename)
  vars = {
    repository_url = var.ecr_repo_url
  }
}

resource "aws_launch_configuration" "mp_app_ecs_launch_config" {
  image_id             = var.image_id //"ami-094d4d00fd7462815"
  iam_instance_profile = var.iam_instance_profile_name // aws_iam_instance_profile.mp_app_ecs_agent.name
  security_groups      = [var.security_group_id] // [aws_security_group.mp_app_staging_ecs_sg.id]
  user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-app-ecs-cluster >> /etc/ecs/ecs.config"
  instance_type        = var.instance_type //"t2.micro"
}

resource "aws_autoscaling_group" "mp_app_ecs_asg" {
  name                      = "mp-${var.cluster_prefix}-asg"
  vpc_zone_identifier       = [var.subnet_id] // [aws_subnet.mp_staging_pub_subnet.id]
  launch_configuration      = aws_launch_configuration.mp_app_ecs_launch_config.name

  desired_capacity          = 1
  min_size                  = 1
  max_size                  = 2
  health_check_grace_period = 300
  health_check_type         = "EC2"
}

resource "aws_ecs_cluster" "mp_app_ecs_cluster" {
  name  = "mp-${var.cluster_prefix}-ecs-cluster"
}

resource "aws_ecs_task_definition" "mp_app_task_definition" {
  family                = var.cluster_prefix
  container_definitions = data.template_file.api_task_definition.rendered
}

resource "aws_ecs_service" "mp_app_ecs_service" {
  name            = var.cluster_prefix
  cluster         = aws_ecs_cluster.mp_app_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_app_task_definition.arn
  desired_count   = 1
}
