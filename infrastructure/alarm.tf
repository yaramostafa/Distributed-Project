resource "aws_cloudwatch_metric_alarm" "cars-dev-scalealarm" {
  alarm_name = "cars-dev-scalealarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods = "2"
  metric_name = "CPUUtilization"
  namespace = "AWS/EC2"
  period = 120
  statistic = "Average"
  threshold = 50

  dimensions = {
    AutoscalingGroupName=aws_autoscaling_group.cars-dev-scalinggroup.name
  }

  alarm_actions = [aws_autoscaling_policy.cars-dev-scalepolicy.arn]
}
