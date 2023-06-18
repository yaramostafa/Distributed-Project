  resource "aws_db_instance" "cars-dev-rds" {
  allocated_storage    = 20
  db_name              = "mydb"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "${var.rds-username}"
  password             = "${var.rds-password}"
  parameter_group_name = "default.mysql5.7"
  vpc_security_group_ids = ["${aws_security_group.cars-dev-securitygroup2.id}"]
  skip_final_snapshot  = true
  publicly_accessible =  true

  provisioner "local-exec" {
    command = "mysql --host=${self.address} --port=${self.port} --user=${self.username} --password=${self.password} mydb < ./demo.sql"
    }
  }

  

