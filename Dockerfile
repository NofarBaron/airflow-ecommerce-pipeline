FROM apache/airflow:3.3.0

USER root

RUN apt-get update && apt-get install -y gcc

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt