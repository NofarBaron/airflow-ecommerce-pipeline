from xmlrpc import client

from google.cloud import bigquery
from pandas.plotting import table
from config.project_config import PROJECT_ID, DATASET

TABLES = [
    "orders",
    "customers",
    "product_catalog",
    "events_sample",
]

UNIQUE_KEYS = { "orders": ["order_id"], 
            #    "customers": [],
                "product_catalog": ["product_id"],
                "events_sample": ["event_id"], }

# Columns that are required and cannot be NULL
REQUIRED_COLUMNS = { "orders": [ "order_id", "customer_id", "product_id", ],
                     "customers": [ "customer_id", "signup_date", ],
                    "product_catalog": [ "product_id", "product_name", ],
                    "events_sample": [ "event_id", "session_id", "event_type", ], }


def validate_row_count(client, table):
    """ Validate that a raw table contains at least one row. """ 
    query = f""" SELECT COUNT(*) AS row_count FROM `{PROJECT_ID}.{DATASET}.{table}` """ 
    row = next(iter(client.query(query).result())) 
    row_count = row.row_count 
    if row_count == 0:
        raise ValueError( f"Data quality check failed: {table} is empty." ) 
    print(f"{table}: {row_count} rows")


def validate_duplicate_keys(client, table, key_columns):
    """ Validate that the configured key columns are unique. """
    columns = ", ".join(key_columns) 
    query = f""" SELECT {columns}, COUNT(*) AS duplicate_count FROM `{PROJECT_ID}.{DATASET}.{table}` GROUP BY {columns} HAVING COUNT(*) > 1 LIMIT 1 """ 
    duplicate = list(client.query(query).result()) 
    if duplicate:
        raise ValueError( f"Data quality check failed: duplicate key found " f"in {table} for column(s): {columns}." ) 
    print(f"{table}: duplicate key check passed") 


def validate_required_columns(client, table, required_columns): 
    """ Validate that required columns do not contain NULL values. """ 
    null_conditions = " OR ".join( f"{column} IS NULL" for column in required_columns ) 
    query = f""" SELECT COUNT(*) AS invalid_rows FROM `{PROJECT_ID}.{DATASET}.{table}` WHERE {null_conditions} """ 
    row = next(iter(client.query(query).result())) 
    invalid_rows = row.invalid_rows
    if invalid_rows > 0:
        raise ValueError( f"Data quality check failed: {table} contains " f"{invalid_rows} row(s) with NULL values in required columns." ) 
    print(f"{table}: NULL validation passed") 


def validate_raw_tables(): 
    """ Run all data quality checks on raw BigQuery tables. 
    The function raises ValueError when a quality check fails. 
    This causes the Airflow validation task to fail and prevents downstream tasks from running. """ 
    client = bigquery.Client() 
    for table in TABLES: 
        # 1. Row count 
        validate_row_count(client, table) 
        # 2. Duplicate key 
        if table in UNIQUE_KEYS:
            validate_duplicate_keys( client, table, UNIQUE_KEYS[table], ) 
        else:
            print(f"{table}: duplicate key check skipped")
        # 3. NULL validation
        validate_required_columns( client, table, REQUIRED_COLUMNS[table], ) 
        print("All raw data quality checks passed.")