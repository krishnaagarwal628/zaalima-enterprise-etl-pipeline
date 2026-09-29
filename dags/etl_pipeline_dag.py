from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Imports from project modules
from extractors.stripe_extractor import extract_stripe
from extractors.salesforce_extractor import extract_salesforce

# Default DAG configuration
default_args = {
    "owner": "zaalima_data_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define main ETL Airflow DAG
with DAG(
    dag_id="zaalima_etl_medallion_pipeline",
    default_args=default_args,
    description="Enterprise Medallion Architecture ETL Pipeline Daily Orchestration",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "medallion", "stripe", "salesforce"],
) as dag:

    # Task 1: Bronze Layer Extraction - Stripe
    extract_stripe_task = PythonOperator(
        task_id="extract_stripe_bronze",
        python_callable=extract_stripe,
    )

    # Task 2: Bronze Layer Extraction - Salesforce
    extract_salesforce_task = PythonOperator(
        task_id="extract_salesforce_bronze",
        python_callable=extract_salesforce,
    )

    # Task execution flow (Parallel extraction)
    [extract_stripe_task, extract_salesforce_task]