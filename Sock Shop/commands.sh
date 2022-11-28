#!/bin/bash

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

sudo docker network create the-network
sudo docker run -d --name front --network the-network -p 9090:8080 --env-file front.env --ip 172.18.0.2 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name one --network the-network -p 9091:8081 --env-file one.env --ip 172.18.0.3 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name two --network the-network -p 9092:8082 --env-file two.env --ip 172.18.0.4 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name three --network the-network -p 9093:8083 --env-file three.env --ip 172.18.0.5 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name four --network the-network -p 9094:8084 --env-file four.env --ip 172.18.0.6 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name five --network the-network -p 9095:8085 --env-file five.env --ip 172.18.0.7 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name six --network the-network -p 9096:8086 --env-file six.env --ip 172.18.0.8 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name seven --network the-network -p 9097:8087 --env-file seven.env --ip 172.18.0.9 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childone --network the-network -p 9098:8088 --env-file childone.env --ip 172.18.0.10 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childtwo --network the-network -p 9099:8089 --env-file childtwo.env --ip 172.18.0.11 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childthree --network the-network -p 9100:8090 --env-file childthree.env --ip 172.18.0.12 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childfour --network the-network -p 9101:8091 --env-file childfour.env --ip 172.18.0.13 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childfivesix --network the-network -p 9102:8092 --env-file childfivesix.env --ip 172.18.0.14 nicholasjackson/fake-service:v0.24.2

sleep 15

curl localhost:9090