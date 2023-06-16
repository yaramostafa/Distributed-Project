resource "aws_vpc" "cars-dev-vpc" {
    cidr_block = "${var.vpc_cidr}"
    instance_tenancy = "default"
  tags = {
    "environment" = "dev"
  }
}
