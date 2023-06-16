resource "aws_autoscaling_policy" "cars-dev-scalepolicy" {
  name = "cars-dev-scalepolicy"
  scaling_adjustment = 1
  adjustment_type = "ChangeInCapacity"
  cooldown = 300
  autoscaling_group_name = "${aws_autoscaling_group.cars-dev-scalinggroup.name}"
}
