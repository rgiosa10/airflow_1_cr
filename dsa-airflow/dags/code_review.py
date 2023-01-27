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

# Prints a welcome statement using the user name
def print_hello():
    with open('/opt/airflow/dags/code_review.txt', 'r') as txt_file:
        contents = txt_file.read()
        print(f"Hello, welcome to this projected completed by {contents}")

# 3 functions that run simultaneously and randomly select an apple from APPLE list
def first_choice():
    choice = random.choice(APPLES)
    print(f"{choice} was chosen")

def second_choice():
    choice = random.choice(APPLES)
    print(f"{choice} was chosen")

def third_choice():
    choice = random.choice(APPLES)
    print(f"{choice} was chosen")

# Set default args for DAG
default_args = {
    'start_date': days_ago(1), # The start date for DAG running
    'schedule_interval': timedelta(days=1), # How often the DAG will run
    'retries': 1, # How many times to retry in case of failure
    'retry_delay': timedelta(seconds=15), # How long to wait before retrying
}

# Create DAG
with DAG(
    'code_review', # a unique name for our DAG
    description='simple DAG with bash, python and dummy tasks', # a description of our DAG
    default_args=default_args, # pass in the default args.
) as dag:
    echo_to_file_task = BashOperator(
        task_id= "echo_to_file",
        bash_command='echo "Ruben Giosa" >> /opt/airflow/dags/code_review.txt',
    )

    greeting_task = PythonOperator(
        task_id = 'greeting',
        python_callable= print_hello,
    )

    echo_task = BashOperator(
        task_id= "echo_three_random_apples",
        bash_command= 'echo "picking three random apples"'
    )

    first_choice_task = PythonOperator(
        task_id = 'first_choice',
        python_callable= first_choice,
    )

    second_choice_task = PythonOperator(
        task_id = 'second_choice',
        python_callable= second_choice,
    )

    third_choice_task = PythonOperator(
        task_id = 'third_choice',
        python_callable= third_choice,
    )

    last_task = DummyOperator(
        task_id = 'last_task'
    )

    # Sets the task order 
    echo_to_file_task >> greeting_task >> echo_task >> [first_choice_task, second_choice_task, third_choice_task] >> last_task