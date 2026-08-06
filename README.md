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
.
├── dags/
├── scripts/
├── sql/
│   ├── staging/
│   ├── facts/
│   ├── marts/
│   └── analysis/
├── config/
├── data/
├── credentials/
└── logs/
```

---

## Pipeline Steps

### 1. Data Ingestion

Raw CSV files are uploaded into BigQuery using Python.

Uploaded tables include:

- orders
- customers
- product_catalog
- events_sample

---

### 2. Validation

After ingestion, validation ensures:

- Raw tables exist
- Required tables contain data
- Pipeline stops if validation fails

---

### 3. Staging Layer

SQL transformations clean and standardize raw data.

Examples:

- Type conversions using SAFE_CAST
- Timestamp normalization
- Status standardization
- Data quality filtering

---

### 4. Warehouse Layer

Fact table:

- fact_events

Mart tables:

- dim_user
- dim_session
- dim_payers

---

## Airflow DAG

The pipeline is orchestrated using Airflow TaskFlow API together with BigQuery operators.

Task dependencies ensure:

```
Upload
   ↓
Validation
   ↓
Staging
   ↓
Facts
   ↓
Marts
```

Independent tasks execute in parallel whenever possible.

---

## Design Decisions

- Raw tables preserve source data.
- Cleaning occurs in the staging layer.
- Business entities are modeled in marts.
- SQL transformations are stored separately from DAG logic.
- Airflow orchestrates execution while BigQuery performs transformations.

---

## Future Improvements

- Task Groups
- Incremental loading using MERGE
- Data quality checks
- Automatic scheduling
- Notifications and monitoring