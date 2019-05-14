default: help

help:
	@echo "Use build and run"

build:
	docker build -t myairflow .

run:
	docker run --rm --name airflow -p 8080:8080 -v ${PWD}/airflow_data:/airflow -e AIRFLOW_HOME=/airflow myairflow

webserver:
	docker exec -it airflow airflow webserver -p 8080

scheduler:
	docker exec -it airflow airflow scheduler

shell:
	docker exec -it airflow bash
