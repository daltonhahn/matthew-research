#!/bin/bash

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

sudo docker network create the-network
sudo docker run -d --name front --net the-network -p 8080:8080 --env-file front.env --ip 172.18.0.2 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name rightfront --net the-network -p 9091:8081 --env-file rightfront.env --ip 172.18.0.3 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name middlefront --net the-network -p 9092:8082 --env-file middlefront.env --ip 172.18.0.4 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name leftfront --net the-network -p 9093:8083 --env-file leftfront.env --ip 172.18.0.5 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name rightleftfront --net the-network -p 9094:8084 --env-file rightleftfront.env --ip 172.18.0.6 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name leftleftfront --net the-network -p 9095:8085 --env-file leftleftfront.env --ip 172.18.0.7 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name childrightfront --net the-network -p 9096:8086 --env-file childrightfront.env --ip 172.18.0.8 nicholasjackson/fake-service:v0.24.2

sleep 5

sudo curl 172.18.0.2:8080