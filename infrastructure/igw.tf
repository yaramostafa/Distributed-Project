resource "aws_internet_gateway" "cars-dev-gateway" {
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"
}
