import os
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

from models.schemas import StripePaymentSchema
from data_lake.storage import save_to_local_lake

# ---------------------------------------------------------
# Retry Decorator: Network errors par 3 attempts tak exponential delay ke sath retry karega
# ---------------------------------------------------------
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=10)
)


def extract_stripe():
    """
    Extract, validate and store a Stripe payment.
    """
    load_dotenv()

    STRIPE_API_URL = os.getenv("STRIPE_API_URL")
    print("Starting Stripe extraction...")
    print(f"Stripe API URL: {STRIPE_API_URL}")

    # ---------------------------------------------------------
    # Simulated raw API payload
    # ---------------------------------------------------------

    raw_payload = {
        "transaction_id": "tx_101",
        "amount": 4999,
        "currency": "USD",
        "customer_email": "customer@example.com",
        "status": "succeeded",
        "created_at": "2026-09-09T10:30:00Z"
    }

    print("Stripe raw payload received.")

    # ---------------------------------------------------------
    # Validate using Pydantic
    # ---------------------------------------------------------

    payment = StripePaymentSchema(
        **raw_payload
    )

    print("Stripe payload validation successful.")

    # ---------------------------------------------------------
    # Convert validated model to JSON-compatible dictionary
    # ---------------------------------------------------------

    validated_data = payment.model_dump(
        mode="json"
    )

    # ---------------------------------------------------------
    # Save to Bronze layer
    # ---------------------------------------------------------

    save_to_local_lake(
        data=validated_data,
        source="stripe",
        filename="stripe_tx_101.json"
    )

    print("Stripe extraction completed successfully.")