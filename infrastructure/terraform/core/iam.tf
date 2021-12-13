// iam role
data "aws_iam_policy_document" "mp_app_ecs_agent" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "mp_app_ecs_agent" {
  name               = "mp_app_ecs_agent"
  assume_role_policy = data.aws_iam_policy_document.mp_app_ecs_agent.json
}

resource "aws_iam_role_policy_attachment" "mp_app_ecs_agent" {
  role       = "aws_iam_role.mp_app_ecs_agent.name"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "mp_app_ecs_agent" {
  name = "ecs-mp_app_ecs_agent"
  role = aws_iam_role.mp_app_ecs_agent.name
}
