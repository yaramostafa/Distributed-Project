#! /bin/bash

yum update -y
yum install python3 -y
pip3 install mysqlclient
yum install git -y
TOKEN="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"
cd /home/ec2-user && git clone https://$TOKEN@github.com/yaramostafa/Distributed-Project.git
python3 -m http.server 1337 &
python3 /home/ec2-user/Distributed-Project/server.py

