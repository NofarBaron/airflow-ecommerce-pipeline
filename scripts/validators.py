from google.cloud import bigquery
from config.project_config import PROJECT_ID, DATASET

TABLES = [
    "orders",
    "customers",
    "product_catalog",
    "events_sample",
]

def validate_raw_tables():
    client = bigquery.Client()

    for table in TABLES:

        query = f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.{table}`
        """

        rows = list(client.query(query).result())

        row_count = rows[0][0]

        if row_count == 0:
            raise ValueError(
                f"{table} is empty!"
            )

        print(f"{table}: {row_count} rows")