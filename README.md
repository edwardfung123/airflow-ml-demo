I lied. This repo has nothing to do with Machine Learning.

# airflow-ml-demo

Start scripts are defined in the `Makefile`.

To avoid polluting my system, I decided to containerized it. The setup is not scalable. For God
sake, please don't use this for production.

---

*It is always a good idea to understand the Makefile before using it.*

`make init` - this will create the "docker network"

`make build` - build the airflow image. This will be used to start the web server and scheduler.

`make run` - run the web server. BUT NOT THE SCHEDULER

`make scheduler` - run the airflow scheduler. If there is no running scheduler, no task can be executed. However, you can still define and update the DAGs without the scheduler.

`make data` - start the Postgres Database. There is a demo task that write data to database.

---

The DAGs are all defined in `airflow_data/dags/`.
