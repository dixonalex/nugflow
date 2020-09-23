# nugflow

This project takes publicly available liquor license data and warehouses it for downstream analysis.

## TODOs

1. Host the analysis & viz online.

## Quickstart

    make run

### Pre-reqs

* docker installed

## Deploy To ECR

1. eval $(aws ecr get-login --region us-east-1 --no-include-email)
2. remake build
3. source .env
4. docker push ${ECR_REPOSITORY_URL}:latest

## SSH Into EC2

1. `terraform apply` in ec2 dir should output ssh command
1. `docker`
  i. this may take a minute to work
  ii. if you are ssh'd in before docker is installed, you'll need to re-ssh in order for the user permissions
  to take effect
1. CONTAINER_ID=$(docker run -d -e NUGFLOW_DATA_PATH=s3://nugflow-usw2-data-lake \
 003793527834.dkr.ecr.us-east-1.amazonaws.com/nugflow-app:latest \
 airflow scheduler)
1. docker exec -ti $CONTAINER_ID bash
1. airflow unpause nugflow_alcohol_colorado
1. airflow trigger_dag nugflow_alcohol_colorado

## Developing

This project is developed under python 3.6.
We use `virtualenv` and `pip` for dependency management.
With these set up, run the following to install deps and run unit tests:

    make init
    make test

## Docs

    make docs

### schemaspy

Make sure pre-reqs are satisfied before running `make docs`.

1. ER Diagram from `vault.db`
   1. Pre-requisites:
      1. sudo apt install graphviz
      1. wget https://github.com/schemaspy/schemaspy/releases/download/v6.0.0/schemaspy-6.0.0.jar
