resource "aws_security_group" "cars-dev-securitygroup2" {
name ="securitygroup2"

ingress{
    from_port=3306
    to_port=3306
    protocol ="tcp"
    cidr_blocks=["${var.all-cidr}"]

}

egress {
    from_port=0
    to_port=0
    protocol ="-1"
    cidr_blocks=["${var.all-cidr}"]

}


}
