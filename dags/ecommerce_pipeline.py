from airflow.decorators import dag, task
from datetime import datetime
import logging


@dag(
    dag_id="ecommerce_elt_pipeline_check",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bigquery", "elt"],
)
def ecommerce_pipeline():

    @task
    def check_new_data():
        logging.info("Checking for new files...")

    @task
    def load_raw_data():
        logging.info("Loading raw data into BigQuery...")

    @task
    def validate_raw_data():
        logging.info("Validating raw tables...")

    @task
    def build_dimensions():
        logging.info("Building dimension tables...")

    @task
    def build_fact_events():
        logging.info("Building fact_events...")

    @task
    def calculate_metrics():
        logging.info("Calculating DAU, MAU and retention...")

    check = check_new_data()
    load = load_raw_data()
    validate = validate_raw_data()
    dims = build_dimensions()
    facts = build_fact_events()
    metrics = calculate_metrics()

    check >> load >> validate >> dims >> facts >> metrics


ecommerce_pipeline()