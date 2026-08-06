# Airflow Project Notes

## Goal

Learn Apache Airflow while converting the previous BigQuery ELT project into a production-style orchestrated pipeline.

---

# Design Decisions

## Why Airflow?

Originally, the pipeline consisted of Python scripts executed manually.

Airflow provides:

- scheduling
- orchestration
- retries
- monitoring
- dependency management

---

## Why BigQuery performs the SQL?

Python uploads the data.

BigQuery performs all transformations.

Advantages:

- compute stays inside BigQuery
- scalable
- SQL is easier to maintain
- follows ELT architecture

---

## Why keep raw tables?

Raw tables preserve source data.

No transformations are applied during ingestion.

Benefits:

- reproducibility
- debugging
- ability to reload downstream tables

---

## Why validate before staging?

If ingestion failed, downstream tables should not be created.

Validation prevents bad data from propagating.

Pipeline:

Upload

↓

Validate

↓

Transform

---

## Why SAFE_CAST instead of CAST?

SAFE_CAST returns NULL instead of failing.

Example:

SAFE_CAST("abc" AS FLOAT64)

returns

NULL

instead of raising an error.

---

## Why not IS_NAN()?

The raw CSV columns were STRING.

IS_NAN only accepts FLOAT64.

Correct approach:

SAFE_CAST(column AS FLOAT64)

---

## Why use dictionaries for SQL tasks?

Instead of manually writing every task:

stg_orders

stg_products

stg_events

we use

STAGING_QUERIES

Advantages:

- less duplicated code
- easier to extend
- DAG remains readable

---

## Why not use loops for upload tasks?

Upload tasks represent business actions.

Each task may later require different logic.

Keeping them explicit improves readability.

SQL tasks are almost identical.

Using a loop there reduces duplication.

---

## Why move run_sql() into another file?

The DAG should describe orchestration only.

Business logic belongs elsewhere.

DAG = workflow

run_sql = implementation

---

## Why SQL files?

Instead of embedding SQL inside Python:

- easier maintenance
- analysts can modify SQL
- closer to production projects

---

## Current Architecture

CSV

↓

Python Upload

↓

Validation

↓

Staging

↓

Fact

↓

Marts

---

# Common Interview Questions

## Why ELT and not ETL?

Because BigQuery performs transformations after loading.

Compute happens inside the warehouse.

---

## Why Airflow?

Scheduling

Retries

Monitoring

Dependencies

Scalability

---

## Why TaskFlow API?

Cleaner code.

Python functions become Airflow tasks.

---

## Why BigQueryInsertJobOperator?

Runs SQL directly inside BigQuery.

Avoids moving data outside the warehouse.

---

## Why SAFE_CAST?

Avoid pipeline failures caused by bad source values.

---

## Why validate after upload?

Ensures downstream transformations only execute on valid data.

---

## Why staging?

Separates raw ingestion from business transformations.

---

## Why raw → staging → facts → marts?

Each layer has one responsibility.

Raw:

exact source

Staging:

clean data

Facts:

events

Marts:

business entities

---

## Why run tasks in parallel?

Independent tables do not need to wait.

Examples:

stg_orders

stg_events

stg_products

can execute simultaneously.

---

## Why does dim_user depend on fact_events?

Because first_seen and total_events are calculated from events.

---

## Why does dim_payers depend only on orders?

It only aggregates purchase information.

---

## Airflow Concepts Learned

- DAG
- Task
- TaskFlow API
- Operators
- Task dependencies
- Scheduler
- Worker
- Triggerer
- Grid View
- Graph View
- Docker deployment
- BigQuery connection
- Logging
- Task retries
- Validation