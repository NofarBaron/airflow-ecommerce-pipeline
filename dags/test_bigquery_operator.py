from datetime import datetime

from airflow.decorators import dag
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
)

@dag(
    dag_id="test_bigquery_operator",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
)
def test_bigquery():

    BigQueryInsertJobOperator(
        task_id="run_test_query",
        gcp_conn_id="google_cloud_default",
        location="US",   # <-- change if your BigQuery dataset is in another region
        configuration={
            "query": {
                "query": """
                SELECT 1 AS test
                """,
                "useLegacySql": False,
            }
        },
    )

test_bigquery()