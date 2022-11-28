#!/bin/bash

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

sudo docker network create the-network
sudo docker run -d --name image1 --net the-network -p 9090:8080 --env-file thing1.env --ip 172.18.0.2 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name image2 --net the-network -p 9091:8081 --env-file thing2.env --ip 172.18.0.3 nicholasjackson/fake-service:v0.24.2
