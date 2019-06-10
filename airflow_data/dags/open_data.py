"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
# from airflow.operators.bash_operator import BashOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

def no_op(text):
    return text




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 10),
    'email': ['edwardfung123@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    'end_date': datetime(3000, 1, 1),
}

# Create a Daily dag
with DAG('open_data', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    fetch_car_parks_task = PythonOperator(
        task_id='fetch_car_parks_task',
        python_callable=no_op,
        provide_context=False
        )

    parse_car_parks_task = PythonOperator(
            task_id='parse_car_parks_task',
            python_callable=no_op,
            provide_context=False
            )

    save_car_parks_task = PythonOperator(
            task_id='save_car_parks_task',
            python_callable=no_op,
            provide_context=False
            )

    visualize = PythonOperator(
            task_id='visualize',
            python_callable=no_op,
            provide_context=False
            )

    fetch_weather_task = PythonOperator(
        task_id='fetch_weather_task',
        python_callable=no_op,
        provide_context=False
        )

    parse_weather_task = PythonOperator(
            task_id='parse_weather_task',
            python_callable=no_op,
            provide_context=False
            )

    save_weather_task = PythonOperator(
            task_id='save_weather_task',
            python_callable=no_op,
            provide_context=False
            )

    fetch_car_parks_task >> parse_car_parks_task >> save_car_parks_task >> visualize
    fetch_weather_task >> parse_weather_task >> save_weather_task >> visualize
