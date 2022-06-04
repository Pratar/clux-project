# Test operator

Creates the basic infrastructure for deploying a web server.

Basic configuration

`k8s-operator/config/samples/ops_v1alpha1_webserver.yaml`

CustomResourceDefinition

`config/crd/bases/ops.test.luxor_webservers.yaml`

Tasks to be performed by the operator

`roles/webserver/tasks/main.yml`



### Starting the project step by step:

git clone project, and build:

1. Build a docker image with a web server

   `cd clux-project`
   
   `docker build -t gcr.io/infra-meta/webserver:0.0.1 .` 
   
   `docker push gcr.io/infra-meta/webserver:0.0.1`

2. Build a operator image

    `cd k8s-operator`
    
    `make docker-build docker-push IMG="gcr.io/infra-meta/k8s-operator:0.0.6"`
    
    `make deploy IMG="gcr.io/infra-meta/k8s-operator:0.0.6"`
    
    `kubectl apply -f config/samples/ops_v1alpha1_webserver.yaml`
    
3. Remove all
   
   `kubectl delete -f config/samples/ops_v1alpha1_webserver.yaml`
   
   `make undeploy`
