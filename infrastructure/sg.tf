resource "aws_security_group" "cars-dev-securitygroup" {
  name = "securitygroup"
  description = "allowing access to machines"
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["${var.all-cidr}"]
  }

    ingress {
    from_port = 10001
    to_port = 10001
    protocol = "tcp"
    cidr_blocks = ["${var.all-cidr}"]
  }

    ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["${var.all-cidr}"]
  }

    ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["${var.all-cidr}"]
  }

    ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["${var.all-cidr}"]
  }

  egress{
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["${var.all-cidr}"]
  }
}
