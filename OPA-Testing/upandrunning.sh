#/bin/bash
cd
cd Desktop/projectsforbardas/matthew-research/OPA-Testing/
minikube config set driver virtualbox
minikube delete
minikube start
minikube kubectl -- get pods -A -o wide
minikube kubectl -- apply -f fake-service1.yaml 
minikube kubectl -- apply -f fake-service2.yaml 
minikube kubectl -- apply -f fake-service3.yaml 
curl $(minikube service fs1 --url) 
