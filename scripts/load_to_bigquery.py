from pathlib import Path
from google.cloud import bigquery
import pandas as pd
import os
from config.project_config import PROJECT_ID, DATASET
import logging

# Project root directory
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/opt/airflow/credentials/service_account.json"
)

def upload_csv(file_path, table_name,ingest_run_id):
    client = bigquery.Client()

    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    logging.info(f"Loading {file_path}")

    df = pd.read_csv(file_path)
    df["ingest_run_id"] = ingest_run_id
    df["ingested_at"] = pd.Timestamp.now(tz="UTC")

    job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            autodetect=True,

    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()

    logging.info(
        f"Loaded {len(df)} rows into {table_name} "
        f"for ingestion run {ingest_run_id}"
    )