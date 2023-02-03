# Configure Minikube to create VirtualBox VM
> minikube config set driver virtualbox
> minikube delete

# Start Minikube
> minikube start

# Check that Kubernetes has come up and pods are listed as "Running"
> minikube kubectl -- get pods -A -o wide

# Install the fake-service files you've created
* Install the fake-serviceX.yaml files one-by-one using the following command

> minikube kubectl -- apply -f \<fileName here\>  

_Angle brackets \<\> are placeholders, do not include those in the command_

# Expose the Fake Service 1 so that you can reach it from your localhost
> minikube service fs1 --url

# Use the URL exposed to curl the system
> curl \<URL from previous command\>
  
_Angle brackets \<\> are placeholders, do not include those in the command_

# Cleanup
> minikube delete