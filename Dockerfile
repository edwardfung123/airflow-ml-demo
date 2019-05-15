FROM python:3.6-slim
RUN apt-get update && apt-get install -y \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install apache-airflow
# install the supporting bundles in a separate line
RUN pip install apache-airflow[postgres]
COPY ./docker-entrypoint.sh /
RUN chmod 700 docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["airflow", "webserver", "-p", "8080"]
