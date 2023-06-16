resource "aws_route_table_association" "cars-dev-routetableassociation1" {
  subnet_id = "${aws_subnet.cars-dev-subnet1.id}"
  route_table_id = "${aws_route_table.cars-dev-routetable.id}"
}

resource "aws_route_table_association" "cars-dev-routetableassociation2" {
  subnet_id = "${aws_subnet.cars-dev-subnet2.id}"
  route_table_id = "${aws_route_table.cars-dev-routetable.id}"
}

resource "aws_route_table_association" "cars-dev-routetableassociation3" {
  subnet_id = "${aws_subnet.cars-dev-subnet3.id}"
  route_table_id = "${aws_route_table.cars-dev-routetable.id}"
}
