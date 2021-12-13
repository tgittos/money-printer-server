
data "template_file" "tr_task_definition" {
  template = file("${path.module}/../task-definitions/task-runner.json.tpl")
  vars = {
    repository_url = aws_ecr_repository.mp_app.repository_url
  }
}

resource "aws_launch_configuration" "mp_worker_ecs_launch_config" {
  image_id             = "ami-094d4d00fd7462815"
  iam_instance_profile = aws_iam_instance_profile.mp_app_ecs_agent.name
  security_groups      = [aws_security_group.mp_app_ecs_sg.id]
  user_data            = "#!/bin/bash\necho ECS_CLUSTER=mp-worker-ecs-cluster >> /etc/ecs/ecs.config"
  instance_type        = "t2.micro"
}

resource "aws_autoscaling_group" "mp_worker_ecs_asg" {
  name                      = "mp-worker-asg"
  vpc_zone_identifier       = [aws_subnet.mp_pub_subnet.id]
  launch_configuration      = aws_launch_configuration.mp_worker_ecs_launch_config.name

  desired_capacity          = 1
  min_size                  = 1
  max_size                  = 10
  health_check_grace_period = 300
  health_check_type         = "EC2"
}

resource "aws_ecs_cluster" "mp_worker_ecs_cluster" {
  name  = "mp-worker-ecs-cluster"
}

resource "aws_ecs_task_definition" "mp_tr_task_definition" {
  family                = "task_runner"
  container_definitions = data.template_file.tr_task_definition.rendered
}

resource "aws_ecs_service" "mp_app_tr_ecs_service" {
  name            = "task-runner"
  cluster         = aws_ecs_cluster.mp_worker_ecs_cluster.id
  task_definition = aws_ecs_task_definition.mp_tr_task_definition.arn
  desired_count   = 1
}
