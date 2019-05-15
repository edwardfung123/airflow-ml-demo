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


mappings = {
    'no': no_op,
    'location': no_op,
    'lat': no_op,
    'lng': no_op,
    'type': no_op,
    'districtL': no_op,
    'districtS': no_op,
    'address': no_op,
    'provider': no_op,
    'parkingNo': no_op,
    'img': no_op,
}


def get_station(station_xml_doc):
    '''
    <no>1</no>
<location>黃大仙中心北館</location>
<lat>22.3425903320313</lat>
<lng>114.190719604492</lng>
<type>SemiQuick</type>
<districtL>九龍</districtL>
<districtS>黃大仙</districtS>
<address>九龍黃大仙龍翔道136號,黃大仙中心北館,三樓停車場,</address>
<provider>CLP</provider>
<parkingNo>320-322</parkingNo>
<img>
/EV/PublishingImages/common/map/map_thumb/Entrance_Lung%20Cheung.jpg
</img>
'''
    return {key: transform_function(station_xml_doc.find(key).text) for key, transform_function in mappings.items()}


def extract_xml_data(**context):
    xml_doc = context['task_instance'].xcom_pull(task_ids='fetch_task')
    # print(xml_doc)
    import xml.etree.ElementTree as ET
    xml_root = ET.fromstring(xml_doc)
    stations = xml_root.find('stationList')
    station_dicts = list(map(get_station, stations.findall('station')))
    from pprint import pprint as pp
    for station in station_dicts:
        pp(station)
    return station_dicts


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 5, 13),
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
with DAG('clp', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    fetch_task = SimpleHttpOperator(
        task_id='fetch_task',
        method='GET',
        http_conn_id='CLP_ELECTRIC_CAR_CHARGER', # https://opendata.clp.com.hk/
        endpoint='GetChargingSectionXML.aspx',
        data=dict(lang='TC'),
        log_response=True,
        xcom_push=True,
        )
    
    parse_task = PythonOperator(
        task_id='parse_task',
        python_callable=extract_xml_data,
        provide_context=True
        )

    sql = '''SELECT 1;
    '''
    save_to_db_task = PostgresOperator(
        task_id='save_to_db_task',
        sql=sql,
        postgres_conn_id='CLP_ELECTRIC_CAR_CHARGER_POSTGRES',
        )

