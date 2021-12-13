
data "template_file" "api_task_definition" {
  template = file("${path.module}/../task-definitions/api.json.tpl")
  vars = {
    repository_url = aws_ecr_repository.mp_app.repository_url
  }
}

resource "aws_launch_configuration" "mp_app_ecs_launch_config" {
  image_id             = "ami-094d4d00fd7462815"
  iam_instance_profile = aws_iam_instance_profile.mp_app_ecs_agent.name
  security_groups      = [aws_security_group.mp_app_ecs_sg.id]
  user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-app-ecs-cluster >> /etc/ecs/ecs.config"
  instance_type        = "t2.micro"
}

resource "aws_autoscaling_group" "mp_app_ecs_asg" {
  name                      = "mp-app-asg"
  vpc_zone_identifier       = [aws_subnet.mp_pub_subnet.id]
  launch_configuration      = aws_launch_configuration.mp_app_ecs_launch_config.name

  desired_capacity          = 1
  min_size                  = 1
  max_size                  = 2
  health_check_grace_period = 300
  health_check_type         = "EC2"
}

resource "aws_ecs_cluster" "mp_app_ecs_cluster" {
  name  = "mp-app-ecs-cluster"
}

resource "aws_ecs_task_definition" "mp_app_task_definition" {
  family                = "app"
  container_definitions = data.template_file.api_task_definition.rendered
}

resource "aws_ecs_service" "mp_app_api_ecs_service" {
  name            = "api"
  cluster         = aws_ecs_cluster.mp_app_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_app_task_definition.arn
  desired_count   = 1
}
