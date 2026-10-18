# Airflow E-commerce ELT Pipeline

## Project Overview

This project demonstrates an end-to-end ELT pipeline orchestrated with Apache Airflow.

The pipeline ingests raw CSV files into BigQuery, validates the loaded data, transforms it through multiple SQL layers, and builds analytical tables following a warehouse architecture.



The goal of the project is to demonstrate production-oriented Data Engineering concepts including:

- Apache Airflow orchestration
- BigQuery ELT workflows
- SQL transformations
- Task dependencies
- Data validation
- Layered warehouse design

---

## Architecture

```
CSV Files
    │
    ▼
Upload Raw Tables (Python)
    │
    ▼
Validate Raw Tables
    │
    ▼
Staging Tables
    │
    ▼
Fact Tables
    │
    ▼
Mart Tables
```

# Airflow DAG

```
ecommerce_elt_pipeline

├── Ingestion
│   ├── upload_orders
│   ├── upload_customers
│   ├── upload_products
│   └── upload_events
│
├── Validation
│
├── Staging
│   ├── stg_orders
│   ├── stg_customers
│   ├── stg_products
│   └── stg_events
│
├── Facts
│   └── fact_events
│
└── Marts
    ├── dim_user
    ├── dim_session
    └── dim_payers
```

The Airflow DAG is organized into five Task Groups:

Ingestion → Validation → Staging → Facts → Marts

---

## Technologies

- Apache Airflow 3
- Google BigQuery
- Python
- Pandas
- Docker
- SQL
- Google Cloud Platform

---

## Project Structure

```
airflow-ecommerce-pipeline/
├── dags/
├── config/
├── scripts/
├── sql/
│   ├── staging/
│   ├── facts/
│   └── marts/
├── data/
├── credentials/
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

---

## Pipeline Steps

### 1. Data Ingestion

CSV files are loaded into BigQuery raw tables.

Each ingestion receives:

- ingest_run_id — identifies the ingestion batch

- ingested_at — ingestion timestamp

---

### 2. Data Quality

The pipeline validates the raw data before transformations:
- Row count checks(Ensures that required tables are not empty.)
- Required NULL checks
- Duplicate key checks (Uniqueness is checked where a business key is expected to be unique.)

The pipeline fails when a critical data-quality check fails.

---

### 3. Staging Layer

SQL transformations clean and standardize raw data.

- Data type conversions
- Timestamp parsing
- Status normalization
- Product category cleaning
- Event type normalization

Example:
```
Raw orders
    │
    ├── order_amount → FLOAT64
    ├── order_date → TIMESTAMP
    ├── status → standardized values
    └── quantity → validated integer
    │
    ▼
stg_orders
```

---

### 4. Warehouse Layer

The transformed staging data is used to create analytical tables.

### Fact

- fact_events

Contains event-level information for analytical queries.

### Dimensions / Marts

- dim_user

Contains customer-level metrics such as:

Total spending
Order counts
Refunded orders

- dim_session

Contains session-level information.

- dim_payers

Contains payer-related information based on orders.

---
# Reliability

The pipeline includes:

- Task retries with a 5-minute delay
- Failure callbacks
- Airflow logging
- Daily scheduling
- Historical backfills

## Retries

Tasks that interact with BigQuery use retries:

```
retries=2
retry_delay=timedelta(minutes=5)
```


This allows temporary failures to recover automatically.
## Scheduling

- The pipeline is configured to run every day at 02:00 (0 2 * * *)

- Catchup is disabled (catchup=False)

This prevents Airflow from automatically creating all historical scheduled runs.

## Backfills

Historical DAG runs can be created using Airflow's backfill functionality.

Example:
```
docker compose exec airflow-scheduler airflow backfill create \
  --dag-id ecommerce_elt_pipeline \
  --from-date 2026-08-22 \
  --to-date 2026-08-23
```

Backfills allow the current DAG logic to be executed for historical logical dates.

## Incremental Loading
The pipeline is designed to support incremental processing using ingest_run_id and ingested_at.

The current development version uses WRITE_TRUNCATE because the source data consists of complete CSV files.

In production, the raw layer could use WRITE_APPEND, followed by incremental processing using MERGE.



---

## Production architecture
In production, raw ingestion could use append-based loading:
```
New Source Batch
       │
       ▼
WRITE_APPEND
       │
       ▼
Raw Historical Data
       │
       ├── ingest_run_id
       └── ingested_at
       │
       ▼
Identify New / Changed Records
       │
       ▼
MERGE
   ┌───┴────┐
   ▼        ▼
MATCHED  NOT MATCHED
   │        │
UPDATE    INSERT
   └───┬────┘
       ▼
   Staging
```




## Design Decisions

- Raw tables preserve source data.
- Cleaning occurs in the staging layer.
- Business entities are modeled in marts.
- SQL transformations are stored separately from DAG logic.
- Airflow orchestrates execution while BigQuery performs transformations.

