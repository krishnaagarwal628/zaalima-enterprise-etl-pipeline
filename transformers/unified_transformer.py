import json
from pathlib import Path
import pandas as pd


def unify_stripe_record(record: dict) -> dict:
    return {
        "transaction_id": record.get("charge_id"),
        "source_system": "stripe",
        "event_timestamp": record.get("created_at"),
        "amount_in_usd": float(record.get("amount", 0.0)),
        "status": record.get("status", "unknown"),
    }


def unify_salesforce_record(record: dict) -> dict:
    return {
        "transaction_id": record.get("opportunity_id"),
        "source_system": "salesforce",
        "event_timestamp": record.get("close_date"),
        "amount_in_usd": float(record.get("amount", 0.0)),
        "status": record.get("stage", "unknown"),
    }


def build_unified_silver_layer(
    stripe_dir: str = "data_lake/silver/stripe",
    sf_dir: str = "data_lake/silver/salesforce",
    output_file: str = "data_lake/silver/unified_silver.json",
):
    unified_records = []

    # Process Stripe
    for file in Path(stripe_dir).glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            records = data if isinstance(data, list) else [data]
            for rec in records:
                unified_records.append(unify_stripe_record(rec))

    # Process Salesforce
    for file in Path(sf_dir).glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            records = data if isinstance(data, list) else [data]
            for rec in records:
                unified_records.append(unify_salesforce_record(rec))

    df_unified = pd.DataFrame(unified_records)

    # Save Unified Output
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_unified.to_json(out_path, orient="records", indent=2)
    print(
        f"[INFO] Unified Silver Layer generated with {len(df_unified)} records at {output_file}"
    )


if __name__ == "__main__":
    build_unified_silver_layer()