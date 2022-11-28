#!/bin/bash

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

sudo docker network create the-network
sudo docker run -d --name loadgenerator --network the-network -p 9090:8080 --env-file loadgenerator.env --ip 172.18.0.2 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name front --network the-network -p 9091:8081 --env-file front.env --ip 172.18.0.3 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name checkout --network the-network -p 9092:8082 --env-file checkout.env --ip 172.18.0.4 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name ad --network the-network -p 9093:8083 --env-file ad.env --ip 172.18.0.5 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name recommendation --network the-network -p 9094:8084 --env-file recommendation.env --ip 172.18.0.6 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name payment --network the-network -p 9095:8085 --env-file payment.env --ip 172.18.0.7 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name email --network the-network -p 9096:8086 --env-file email.env --ip 172.18.0.8 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name productcatalog --network the-network -p 9097:8087 --env-file productcatalog.env --ip 172.18.0.9 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name shipping --network the-network -p 9098:8088 --env-file shipping.env --ip 172.18.0.10 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name currency --network the-network -p 9099:8089 --env-file currency.env --ip 172.18.0.11 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name cart --network the-network -p 9100:8090 --env-file cart.env --ip 172.18.0.12 nicholasjackson/fake-service:v0.24.2
sudo docker run -d --name redis_cache --network the-network -p 9101:8091 --env-file redis_cache.env --ip 172.18.0.13 nicholasjackson/fake-service:v0.24.2

sleep 15

curl localhost:9090