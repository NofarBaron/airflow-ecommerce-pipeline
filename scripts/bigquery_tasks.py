from datetime import timedelta
import logging
from pathlib import Path
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.decorators import task

SQL_DIR = Path("/opt/airflow/sql")


def run_sql(task_id: str, sql_file: str):
    logging.info(
        f"Creating BigQuery task {task_id} "
        f"using SQL file {sql_file}"
    )

    return BigQueryInsertJobOperator(
        task_id=task_id,
        gcp_conn_id="google_cloud_default",
        location="US",
        retries=2,
        retry_delay=timedelta(minutes=5),
        configuration={
            "query": {
                "query": (SQL_DIR / sql_file).read_text(),
                "useLegacySql": False,
            }
        },
    )