from pathlib import Path
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

SQL_DIR = Path("/opt/airflow/sql")


def run_sql(task_id: str, sql_file: str):
    return BigQueryInsertJobOperator(
        task_id=task_id,
        gcp_conn_id="google_cloud_default",
        location="US",
        configuration={
            "query": {
                "query": (SQL_DIR / sql_file).read_text(),
                "useLegacySql": False,
            }
        },
    )