from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import aft_to_csv
from scripts.retrain import retrain_after_updated

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

with DAG(
    dag_id='anime_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for anime dataset using Airflow 🌀',
    schedule_interval='@hourly',
    catchup=False,
    tags=['anime', 'etl']
) as dag:

    extract = extract_data()
    transform = transform_data()
    load = aft_to_csv()
    retrain = retrain_after_updated()
    
    extract >> transform >> load >> retrain
