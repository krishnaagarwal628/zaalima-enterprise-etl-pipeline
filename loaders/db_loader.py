import json
import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import UnifiedTransaction


def load_silver_json_to_db(json_filepath: str) -> int:
    """Reads Silver layer cleaned JSON data and inserts records into the Database.

    Returns the count of successfully loaded records.
    """
    if not os.path.exists(json_filepath):
        print(f"[ERROR] File not found: {json_filepath}")
        return 0

    with open(json_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    records: List[Dict[str, Any]] = data if isinstance(data, list) else [data]

    # Infer source system from path if missing in record
    fallback_source = "stripe" if "stripe" in json_filepath.lower() else "salesforce"

    db: Session = SessionLocal()
    inserted_count = 0

    try:
        for record in records:
            source = record.get("source_system") or fallback_source

            transaction = UnifiedTransaction(
                transaction_id=str(record.get("transaction_id", record.get("id"))),
                source_system=source,
                event_timestamp=str(record.get("event_timestamp", record.get("created_at", ""))),
                amount_in_usd=float(record.get("amount_in_usd", record.get("amount", 0.0))),
                status=record.get("status", "unknown"),
            )
            db.add(transaction)
            inserted_count += 1

        db.commit()
        print(f"[SUCCESS] Successfully inserted {inserted_count} records into the database.")
        return inserted_count

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to load data into database: {e}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sample_silver_path = "data_lake/silver/stripe/stripe_tx_101_clean.json"
    if os.path.exists(sample_silver_path):
        load_silver_json_to_db(sample_silver_path)
    else:
        print(f"[INFO] Test file {sample_silver_path} not found.")