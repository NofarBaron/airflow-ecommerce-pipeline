from datetime import datetime, timedelta
import logging
import uuid
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

from scripts.load_to_bigquery import upload_csv
from scripts.validators import validate_raw_tables 
from pathlib import Path
from scripts.bigquery_tasks import run_sql
from config.pipeline_config import (
    STAGING_QUERIES,
    FACT_QUERIES,
    MART_QUERIES,
)

DEFAULT_RETRY_DELAY = timedelta(minutes=5)
DATA_DIR = Path("/opt/airflow/data")


def task_failure_alert(context):
    task_instance = context["task_instance"]

    logging.error(
        f"""
        TASK FAILURE
        DAG: {task_instance.dag_id}
        Task: {task_instance.task_id}
        Run: {task_instance.run_id}
        Logical Date: {task_instance.logical_date}
        Try Number: {task_instance.try_number}
        """
    )

default_args = {
    "retries": 3,
    "retry_delay": DEFAULT_RETRY_DELAY,
    "on_failure_callback": task_failure_alert,
}

@dag(
    dag_id="ecommerce_elt_pipeline",
    start_date=datetime(2026, 1, 1),
    # schedule=None,
    schedule="0 2 * * *", ##to run every day at 2:00, but for testing we can set it to None
    catchup=False,
    default_args=default_args,
    dagrun_timeout=timedelta(hours=1),
    tags=["bigquery", "ecommerce"],
)

def ecommerce_pipeline():
    
    @task
    def generate_ingest_run_id():
        return str(uuid.uuid4())

    ingest_run_id = generate_ingest_run_id()

    #for testing the retry behavior of Airflow, we can create a task that will always fail
    # @task(retries=0)
    # def test_retry():
    #     raise ValueError("Testing Airflow retry behavior")
    
    # retry_test = test_retry()


    @task
    def upload_table(file_name: str, table_name: str):
        logging.info(f"Uploading {table_name}")
        file_path = DATA_DIR / file_name
        upload_csv(str(file_path), table_name)


    # =========================  Ingestion ========================= 
    with TaskGroup(group_id="ingestion") as ingestion:
        orders = upload_table.override(task_id="upload_orders")("orders.csv","orders")
        customers = upload_table.override(task_id="upload_customers")("customers.csv","customers")
        products = upload_table.override(task_id="upload_products")("product_catalog.csv", "product_catalog")
        events = upload_table.override(task_id="upload_events")("clickstream_events_sample.csv","events_sample")


    # =========================  Validation ========================= 
    with TaskGroup(group_id="validation") as validation:
        @task(task_id="validate_raw_tables", retries=0) 
        def validate(): 
            validate_raw_tables() 
        validate_raw = validate()


   # =========================  Staging ========================= 
    with TaskGroup(group_id="staging") as staging: 
        staging_tasks = {} 
        for task_id, sql_file in STAGING_QUERIES.items():
            staging_tasks[task_id] = run_sql(task_id, sql_file)


   # ========================= Facts ========================= 
    with TaskGroup(group_id="facts") as facts: 
        fact_tasks = {}
        for task_id, sql_file in FACT_QUERIES.items():
            fact_tasks[task_id] = run_sql(task_id, sql_file)


    # ========================= Marts ========================= 
    with TaskGroup(group_id="marts") as marts:
        mart_tasks = {} 
        for task_id, sql_file in MART_QUERIES.items():
            mart_tasks[task_id] = run_sql(task_id, sql_file)


    ingestion >> validation 

    # ingestion >> retry_test

    validation >> staging

    staging_tasks["stg_events"] >> facts
    staging_tasks["stg_orders"] >> mart_tasks["dim_payers"] 

    [ staging_tasks["stg_orders"], fact_tasks["fact_events"], ] >> mart_tasks["dim_user"] 
    fact_tasks["fact_events"] >> mart_tasks["dim_session"]


ecommerce_pipeline()