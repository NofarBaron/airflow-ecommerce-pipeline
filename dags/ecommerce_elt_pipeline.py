from datetime import datetime
import logging

from airflow.decorators import dag, task
from scripts.load_to_bigquery import upload_csv
from scripts.validators import validate_raw_tables 
from pathlib import Path
from scripts.bigquery_tasks import run_sql
from config.pipeline_config import (
    STAGING_QUERIES,
    FACT_QUERIES,
    MART_QUERIES,
)
DATA_DIR = Path("/opt/airflow/data")


@dag(
    dag_id="ecommerce_elt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bigquery", "ecommerce"],
)
def ecommerce_pipeline():

    @task
    def upload_table(file_name: str, table_name: str):
        logging.info(f"Uploading {table_name}")

        file_path = DATA_DIR / file_name

        upload_csv(str(file_path), table_name)
    
    orders = upload_table.override(task_id="upload_orders")("orders.csv","orders",)

    customers = upload_table.override(task_id="upload_customers")(
        "customers.csv",
        "customers",
    )

    products = upload_table.override(task_id="upload_products")(
        "product_catalog.csv",
        "product_catalog",
    )

    events = upload_table.override(task_id="upload_events")(
        "clickstream_events_sample.csv",
        "events_sample",
    )

    @task
    def validate():
        validate_raw_tables()

    validation = validate()
   
    staging_tasks = {}
    for task_id, sql_file in STAGING_QUERIES.items():
        staging_tasks[task_id] = run_sql(task_id, sql_file)

    fact_tasks = {}
    for task_id, sql_file in FACT_QUERIES.items():
        fact_tasks[task_id] = run_sql(task_id, sql_file)

    mart_tasks = {}
    for task_id, sql_file in MART_QUERIES.items():
        mart_tasks[task_id] = run_sql(task_id, sql_file)


    [orders, customers, products, events] >> validation
    validation >> list(staging_tasks.values())

    staging_tasks["stg_events"] >> fact_tasks["fact_events"]

    staging_tasks["stg_orders"] >> mart_tasks["dim_payers"]

    [
        staging_tasks["stg_orders"],
        fact_tasks["fact_events"],
    ] >> mart_tasks["dim_user"]

    fact_tasks["fact_events"] >> mart_tasks["dim_session"]

ecommerce_pipeline()