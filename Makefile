IMAGE_NAME := myairflow
CONTAINER_NAME := airflow

default: help

help:
	@echo "Use build and run"

build:
    # Build the docker image
	docker build -t ${IMAGE_NAME} .

run:
	# initialize the airflow database and start the airflow web server
	# see docker-entrypoint.sh
	docker run --rm --name ${CONTAINER_NAME} -p 8080:8080 \
		-v ${PWD}/airflow_data:/airflow \
		-e AIRFLOW_HOME=/airflow \
		${IMAGE_NAME}

webserver:
	# Starting the web server
	docker exec -it ${CONTAINER_NAME} airflow webserver -p 8080

scheduler:
	# Starting the scheduler. Without the scheduler no job can be run
	docker exec -it ${CONTAINER_NAME} airflow scheduler

shell:
	# Spawn a bash shell so that we can interact with the airflow with CLI.
	docker exec -it ${CONTAINER_NAME} bash

stop:
	docker stop ${CONTAINER_NAME}