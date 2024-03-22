python-function-kubernetes-ci-cd
This repo shows a http_trigger in python deployed as Azure Function in Azure App Service and containerized and deployed in Azure Kubernetes Service through Azure DevOps pipelines. There are two parts in the demo. We first create a python function and run it locally and then in Azure. Afterward, we containerize the function and test it locally and then push the image to Azure and run the image in AKS (Azure Kubernetes Service). The deployment are done first manually and then with CI/CD pipeline in ADO (Azure DevOps).

Uncontainerized Python Function
Create http_triger in python and test it as a function locally
Create a new directory and CD in
Start VS Code with code .
Install plug-in for Azure Function
Use the prompt to create a python function for http_trigger
Make sure the Azure Function Utility is installed on you machine and check it version:
func --version
4.0.5455
With VS Code you can write a http_trigger in python and run it locally with Azure Function CLI:
func start
Using Postman, hit the function with URL of
http://127.0.0.1:7071/api/http_trigger
And body
{ "name": "Jack Xue 2024-03-04" }
Deploy the function into Azure App Service
Create Azure App Service Plan
From VS Code, folloiwng promp to deployt the function in the App Servcie Plan.
Using Postman to hit the function in Azure:
https://jackfunc.azurewebsites.net/api/http_trigger
Create yaml file for using ADO CI/CD pipeline to build and deploy the function ino Azure
Create a yaml file func-ase-ci-cd.yml for build and deploy the python function in to the service plan.
Check the code into Azure DevOps
Create a project in ADO
Check in all files in the directory into ADO git add . git commit -m "Check in all files" git push origin
Using pipeline to trig a deployment in Azure
Make a small and tracible change in python code, such as a log statement
Save you change and push/sync your code with its remote branch.
The pipeline was trigged as it saw a change in main branch.
Using Postman to hit the function in Azure:
https://jackfunc.azurewebsites.net/api/http_trigger
You should see your change either in response or in log.
Containerize the Python Function
Dockerize the function and test it locally
Use function cli generate Docker file
func init --docker-only
Make sure docker desktop is stalled and started for Linux containers.
Build the image with
docker build -t httptrigger .
Run the image locally
docker run -p 8080:80 -it httptrigger:latest
Use Postman, hit the containerized function with URL of
http://127.0.0.1:8080/api/http_trigger
And body
{ "name": "Xue from local docker 2024-03-04" }
Push the image to AKs manually
Log into Azure portal and create
Azure Container Registry, jackcontainerreg
Azure Kubernetes Service, jackaks
From the current directory log into Azure and run
az login
az account set --subscription
az acr login --name jackcontainerreg
Push the image to ACR
docker tag httptrigger:latest jackcontainerreg.azurecr.io/httptrigger:latest
docker push jackcontainerreg.azurecr.io/httptrigger:latest
Connect ACR and AKS
az acr update -n jackcontainerreg --admin-enabled true
az aks update -n jackaks -g jackrg --attach-acr jackcontainerreg
Enable run kubectl locally
az aks get-credentials -g zediproin -n zediproinaks
Deploy the ACR image to AKS
For first creation: kubectl apply -f func-kerctl-aks.yml
For subsequent update: kubectl rollout restart -f func-kerctl-aks.yml --namespace=default
Using Postman to hit the containerized function in Azure:
http://57.151.53.186:80/api/http_trigger
Notice: the IP address may be different. You can get the right one form AKS Service panel.
Push a change to the repo and trig a deployment
Log into ADO
Create a new pipeline and set the trigger to the main branch and use the yaml file func-kerctl-aks.yml
Make a change in the python code
Push and sync the code with the repo which will trig the CI/CD pipeline
Once the deployment finished, using Postman to verify the containerized function
http://57.151.53.186:80/api/http_trigger
Notice: the IP address may be different. You can get the right one form AKS Service panel.
