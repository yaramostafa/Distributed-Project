resource "aws_route_table" "cars-dev-routetable" {
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.cars-dev-gateway.id}"
  }

  tags={
    environment="dev"
  }
}
