resource "aws_autoscaling_group" "cars-dev-scalinggroup" {
    name = "${aws_launch_configuration.cars-dev-launchtemplate.name}-asg"
    min_size = 1
    desired_capacity = 2
    max_size = 5
    health_check_type = "ELB"
    load_balancers = ["${aws_elb.cars-dev-loadbalancer.id}"]
    launch_configuration = "${aws_launch_configuration.cars-dev-launchtemplate.name}"
    enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances"
  ]



  vpc_zone_identifier  = [
    "${aws_subnet.cars-dev-subnet1.id}",
    "${aws_subnet.cars-dev-subnet2.id}",
    "${aws_subnet.cars-dev-subnet3.id}"
  ]
   lifecycle {
    create_before_destroy = true
  }

  tag {
    key ="environment"
    value ="dev"
    propagate_at_launch = true
  }

  
}
