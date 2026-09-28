import json
import os
import pytest
from database.connection import SessionLocal
from database.init_db import init_db
from database.models import UnifiedTransaction
from loaders.db_loader import load_silver_json_to_db


@pytest.fixture(autouse=True)
def setup_test_database():
    """Ensure database tables exist before running loader tests."""
    init_db()


def test_load_silver_json_to_db_success(tmp_path):
    """Verify that valid silver JSON data is successfully upserted into the database."""
    # 1. Mock sample silver record in a temporary file
    test_file = tmp_path / "test_stripe_clean.json"
    sample_data = {
        "transaction_id": "tx_test_999",
        "source_system": "stripe",
        "event_timestamp": "2026-09-28 10:00:00",
        "amount_in_usd": 150.75,
        "status": "succeeded",
    }
    test_file.write_text(json.dumps(sample_data), encoding="utf-8")

    # 2. Run loader function
    loaded_count = load_silver_json_to_db(str(test_file))
    assert loaded_count == 1

    # 3. Query DB to verify persistence
    db = SessionLocal()
    try:
        record = (
            db.query(UnifiedTransaction)
            .filter_by(transaction_id="tx_test_999")
            .first()
        )
        assert record is not None
        assert record.source_system == "stripe"
        assert record.amount_in_usd == 150.75
        assert record.status == "succeeded"
    finally:
        db.close()


def test_upsert_idempotency_update(tmp_path):
    """Verify that re-loading a transaction with updated details modifies the existing row

    instead of failing or creating duplicates.
    """
    test_file = tmp_path / "test_stripe_upsert.json"

    # Initial Insert
    initial_data = {
        "transaction_id": "tx_test_999",
        "source_system": "stripe",
        "event_timestamp": "2026-09-28 10:00:00",
        "amount_in_usd": 150.75,
        "status": "pending",
    }
    test_file.write_text(json.dumps(initial_data), encoding="utf-8")
    load_silver_json_to_db(str(test_file))

    # Updated Record (Same transaction_id, status changed to 'succeeded')
    updated_data = {
        "transaction_id": "tx_test_999",
        "source_system": "stripe",
        "event_timestamp": "2026-09-28 10:05:00",
        "amount_in_usd": 150.75,
        "status": "succeeded",
    }
    test_file.write_text(json.dumps(updated_data), encoding="utf-8")

    # Perform Upsert
    loaded_count = load_silver_json_to_db(str(test_file))
    assert loaded_count == 1

    # Query DB to verify that the status updated and no duplicate was created
    db = SessionLocal()
    try:
        records = (
            db.query(UnifiedTransaction)
            .filter_by(transaction_id="tx_test_999")
            .all()
        )
        assert len(records) == 1  # Ensures idempotency (no duplication)
        assert records[0].status == "succeeded"
    finally:
        db.close()


def test_load_non_existent_file():
    """Verify that providing an invalid file path returns 0 without crashing."""
    loaded_count = load_silver_json_to_db("data_lake/non_existent_file.json")
    assert loaded_count == 0