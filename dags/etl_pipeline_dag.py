import glob
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Project Imports
from database.init_db import init_db
from extractors.salesforce_extractor import extract_salesforce
from extractors.stripe_extractor import extract_stripe
from loaders.db_loader import load_silver_json_to_db
from transformers.salesforce_transformer import batch_transform_salesforce_dir
from transformers.stripe_transformer import batch_transform_stripe_dir

default_args = {
    "owner": "zaalima_data_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def load_all_silver_to_gold():
    """Reads all cleaned JSON files from Silver directory and loads into Gold DB."""
    init_db()
    total_loaded = 0

    silver_stripe_pattern = os.path.join(
        "data_lake", "silver", "stripe", "*.json"
    )
    for file_path in glob.glob(silver_stripe_pattern):
        total_loaded += load_silver_json_to_db(file_path)

    silver_sf_pattern = os.path.join(
        "data_lake", "silver", "salesforce", "*.json"
    )
    for file_path in glob.glob(silver_sf_pattern):
        total_loaded += load_silver_json_to_db(file_path)

    print(f"[Airflow Task] Gold Layer Sync Completed. Total Records: {total_loaded}")


with DAG(
    dag_id="zaalima_etl_medallion_pipeline",
    default_args=default_args,
    description="Enterprise Medallion Architecture ETL Pipeline Daily Orchestration",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "medallion", "stripe", "salesforce"],
) as dag:

    # --- Phase 1: Bronze Layer Tasks ---
    extract_stripe_task = PythonOperator(
        task_id="extract_stripe_bronze",
        python_callable=extract_stripe,
    )

    extract_salesforce_task = PythonOperator(
        task_id="extract_salesforce_bronze",
        python_callable=extract_salesforce,
    )

    # --- Phase 2: Silver Layer Tasks ---
    transform_stripe_task = PythonOperator(
        task_id="transform_stripe_silver",
        python_callable=batch_transform_stripe_dir,
    )

    transform_salesforce_task = PythonOperator(
        task_id="transform_salesforce_silver",
        python_callable=batch_transform_salesforce_dir,
    )

    # --- Phase 3: Gold Layer Task ---
    load_gold_task = PythonOperator(
        task_id="load_gold_warehouse",
        python_callable=load_all_silver_to_gold,
    )

    # --- Task Dependencies Setup ---
    # 1. Stripe Bronze -> Silver
    extract_stripe_task >> transform_stripe_task

    # 2. Salesforce Bronze -> Silver
    extract_salesforce_task >> transform_salesforce_task

    # 3. Both Silver Transformations -> Gold Warehouse Sync
    [transform_stripe_task, transform_salesforce_task] >> load_gold_task