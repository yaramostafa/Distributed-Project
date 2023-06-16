resource "aws_elb" "cars-dev-loadbalancer" {
    name = "cars-dev-loadbalancer"
    security_groups = [
        "${aws_security_group.cars-dev-securitygroup.id}"
    ]

    subnets = [
        "${aws_subnet.cars-dev-subnet1.id}",
        "${aws_subnet.cars-dev-subnet2.id}",
        "${aws_subnet.cars-dev-subnet3.id}"
    ]
    cross_zone_load_balancing = true
health_check {
    healthy_threshold = 2
    unhealthy_threshold = 2
    timeout = 3
    interval = 30
    target = "HTTP:80/"
  }
listener {
    lb_port = 80
    lb_protocol = "http"
    instance_port = "80"
    instance_protocol = "http"
  }
listener {
    lb_port = 10001
    lb_protocol = "tcp"
    instance_port = "10001"
    instance_protocol = "tcp"
  }

}
