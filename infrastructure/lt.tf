resource "aws_launch_configuration" "cars-dev-launchtemplate" {
  name_prefix = "cars-dev-"
  image_id = "ami-022e1a32d3f742bd8"
  instance_type = "t2.micro"
  key_name = "cars-dev-key"

  security_groups=["${aws_security_group.cars-dev-securitygroup.id}"]
  associate_public_ip_address=true
  user_data="${file("data.sh")}"
  lifecycle {
    create_before_destroy = true
  }
}

