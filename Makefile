AIRFLOW_IMAGE_NAME := myairflow
AIRFLOW_CONTAINER_NAME := airflow

POSTGRES_IMAGE_NAME := postgres:11
POSTGRES_CONTAINER_NAME := postgres

DOCKER_NETWORK_NAME := test_airflow


default: help

help:
	@echo "Use build and run"

init:
	docker network create ${DOCKER_NETWORK_NAME}

build:
    # Build the docker image
	docker build -t ${AIRFLOW_IMAGE_NAME} .

run:
	# initialize the airflow database and start the airflow web server
	# see docker-entrypoint.sh
	docker run --rm --name ${AIRFLOW_CONTAINER_NAME} -p 8080:8080 \
	    --network ${DOCKER_NETWORK_NAME} \
		-v ${PWD}/airflow_data:/airflow \
		-e AIRFLOW_HOME=/airflow \
		${AIRFLOW_IMAGE_NAME}

webserver:
	# Starting the web server
	docker exec -it ${AIRFLOW_CONTAINER_NAME} airflow webserver -p 8080

scheduler:
	# Starting the scheduler. Without the scheduler no job can be run
	docker exec -it ${AIRFLOW_CONTAINER_NAME} airflow scheduler

shell:
	# Spawn a bash shell so that we can interact with the airflow with CLI.
	docker exec -it ${AIRFLOW_CONTAINER_NAME} bash

stop:
	docker stop ${AIRFLOW_CONTAINER_NAME}

database:
	docker run --rm --name ${POSTGRES_CONTAINER_NAME} \
		--network ${DOCKER_NETWORK_NAME} \
		-v ${PWD}/postgres_data:/var/lib/postgresql/data \
		-p 5432:5432 \
		-e POSTGRES_PASSWORD=root \
		${POSTGRES_IMAGE_NAME}

test_db:
	docker run -it --rm --network ${DOCKER_NETWORK_NAME} ${POSTGRES_IMAGE_NAME} \
		psql -h ${POSTGRES_CONTAINER_NAME} -U postgres