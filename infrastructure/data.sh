#! /bin/bash

yum update -y
yum install python3 -y
dnf install -y pip
dnf install -y mariadb105-devel gcc python3-devel
pip install mysqlclient
yum install git -y
TOKEN="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"
cd /home/ec2-user && git clone https://$TOKEN@github.com/yaramostafa/Distributed-Project.git
python3 -m http.server 1337 &
python3 /home/ec2-user/Distributed-Project/ChatServer.py &
python3 /home/ec2-user/Distributed-Project/CarServer.py &
