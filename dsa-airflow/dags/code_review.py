from datetime import timedelta, datetime

from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago 
import pandas as pd
import os
import sys
import json
import random

APPLES = ["pink lady", "jazz", "orange pippin", "granny smith", "red delicious", "gala", "honeycrisp", "mcintosh", "fuji"]

default_args = {
    'start_date': days_ago(1), # The start date for DAG running
    'schedule_interval': timedelta(days=1), # How often the DAG will run
    'retries': 1, # How many times to retry in case of failure
    'retry_delay': timedelta(seconds=15), # How long to wait before retrying
}






with DAG(
    'code_review', # a unique name for our DAG
    description='ETL DAG for world_happiness_index csv to json', # a description of our DAG
    default_args=default_args, # pass in the default args.
) as dag:
    echo_to_file_task = BashOperator(
        task_id= "echo_to_file",
        bash_command='echo "Ruben Giosa" >> /opt/airflow/dags/code_review.txt',
    )

    greeting_task = PythonOperator(
        task_id = 'greeting'
    )

    