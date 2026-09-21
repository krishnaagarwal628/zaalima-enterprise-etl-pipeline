import pytest
from transformers.unified_transformer import (
    unify_salesforce_record,
    unify_stripe_record,
)


def test_unify_stripe_record():
    raw_stripe = {
        "charge_id": "ch_123",
        "amount": 100.50,
        "created_at": "2026-09-01T10:00:00Z",
        "status": "succeeded",
    }
    unified = unify_stripe_record(raw_stripe)

    assert unified["transaction_id"] == "ch_123"
    assert unified["source_system"] == "stripe"
    assert unified["amount_in_usd"] == 100.50
    assert unified["status"] == "succeeded"


def test_unify_salesforce_record():
    raw_sf = {
        "opportunity_id": "00680000001",
        "amount": 5000.00,
        "close_date": "2026-09-15",
        "stage": "Closed Won",
    }
    unified = unify_salesforce_record(raw_sf)

    assert unified["transaction_id"] == "00680000001"
    assert unified["source_system"] == "salesforce"
    assert unified["amount_in_usd"] == 5000.00
    assert unified["status"] == "Closed Won"