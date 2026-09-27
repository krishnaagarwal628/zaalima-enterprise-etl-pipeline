from database.init_db import init_db
from loaders.db_loader import load_silver_json_to_db
import glob
import os
from extractors.salesforce_extractor import extract_salesforce
from extractors.stripe_extractor import extract_stripe
from transformers.salesforce_transformer import batch_transform_salesforce_dir
from transformers.stripe_transformer import batch_transform_stripe_dir


def main():

    print("=" * 60)
    print("ZAALIMA ETL PIPELINE - BRONZE TO SILVER")
    print("Pipeline Started")
    print("=" * 60)

    # ---------------------------------------------------------
    # PHASE 1: Bronze Ingestion
    # ---------------------------------------------------------
    print("\n[PHASE 1] Running Extractor Ingestion (Bronze Layer)...")

    print("\n[1/2] Running Stripe extractor...")
    try:
        extract_stripe()
        print("Stripe extraction: SUCCESS")
    except Exception as error:
        print(f"Stripe extraction: FAILED - {error}")

    print("\n[2/2] Running Salesforce extractor...")
    try:
        extract_salesforce()
        print("Salesforce extraction: SUCCESS")
    except Exception as error:
        print(f"Salesforce extraction: FAILED - {error}")

    # ---------------------------------------------------------
    # PHASE 2: Silver Transformation
    # ---------------------------------------------------------
    print("\n[PHASE 2] Running Batch Transformers (Silver Layer)...")

    print("\n[1/2] Running Stripe Transformer...")
    try:
        batch_transform_stripe_dir()
        print("Stripe transformation: SUCCESS")
    except Exception as error:
        print(f"Stripe transformation: FAILED - {error}")

    print("\n[2/2] Running Salesforce Transformer...")
    try:
        batch_transform_salesforce_dir()
        print("Salesforce transformation: SUCCESS")
    except Exception as error:
        print(f"Salesforce transformation: FAILED - {error}")

    # ---------------------------------------------------------
    # PHASE 3: Gold Warehouse Sync (Upsert to DB)
    # ---------------------------------------------------------
    print("\n[PHASE 3] Loading Cleaned Silver Data into Gold Warehouse...")
    
    # Initialize DB tables if not exist
    init_db()

    total_loaded = 0

    # Sync Stripe Silver Cleaned Files
    silver_stripe_pattern = os.path.join("data_lake", "silver", "stripe", "*.json")
    for file_path in glob.glob(silver_stripe_pattern):
        total_loaded += load_silver_json_to_db(file_path)

    # Sync Salesforce Silver Cleaned Files
    silver_sf_pattern = os.path.join("data_lake", "silver", "salesforce", "*.json")
    for file_path in glob.glob(silver_sf_pattern):
        total_loaded += load_silver_json_to_db(file_path)

    print(f"\n[Gold Layer] Total Records Synced: {total_loaded}")

    # ---------------------------------------------------------
    # Pipeline completed
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("ETL Pipeline Execution Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()