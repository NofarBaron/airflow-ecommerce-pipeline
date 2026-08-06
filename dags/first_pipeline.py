from airflow.decorators import dag, task
from datetime import datetime
import logging


@dag(
    dag_id="first_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning"],
)
def first_pipeline():

    @task
    def check_data():
        logging.info("Checking data...")
        return "Data found"

    @task
    def validate_data(message):
        logging.info(f"Validating: {message}")

    @task
    def prepare_report():
        logging.info("Preparing report...")

    @task
    def archive_logs():
        logging.info("Archiving logs...")

    @task
    def finish():
        logging.info("Pipeline completed!")

    data = check_data()

    validation = validate_data(data)

    report = prepare_report()
    archive = archive_logs()

    validation >> [report, archive]

    [report, archive] >> finish()


first_pipeline()