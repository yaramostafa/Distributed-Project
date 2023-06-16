resource "aws_subnet" "cars-dev-subnet1" {
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"
  cidr_block = "${vars.vpc-cidr-subnet1}"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"

tags{
    environment="dev"
}

}

resource "aws_subnet" "cars-dev-subnet2" {
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"
  cidr_block = "${vars.vpc-cidr-subnet2}"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1b"

tags{
    environment="dev"
}

}

resource "aws_subnet" "cars-dev-subnet3" {
  vpc_id = "${aws_vpc.cars-dev-vpc.id}"
  cidr_block = "${vars.vpc-cidr-subnet3}"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1c"

tags{
    environment="dev"
}

}
