import os
import time
import sys 
from dotenv import load_dotenv

# Path resolution for root imports execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Global environment variables load 
load_dotenv()
STRIPE_API_URL = os.getenv("STRIPE_API_URL")

from models.schemas import StripePaymentSchema
from data_lake.storage import save_to_local_lake


def fetch_strip_page(starting_after = None):
    """
    Simulate paginated responses from Strip API using cursor logic (starting_after). 
    """
    if starting_after is None:
        #page 1 API response 
        return{
            "object": "list",
            "has_more": True,
            "data": [
                {
                    "transaction_id": "tx_101",
                    "amount": 4999,
                    "currency": "USD",
                    "customer_email": "customer@example.com",
                    "status": "succeeded",
                    "created_at": "2026-09-09T10:30:00Z"
                },
               {
                    "transaction_id": "tx_102",
                    "amount": 2999,
                    "currency": "USD",
                    "customer_email": "customer2@example.com",
                    "status": "succeeded",
                    "created_at": "2026-09-09T11:00:00Z"
                }
            ]
        }
    else:
        #page 2 API response 
        return {
            "object": "list",
            "has_more": False,
            "data": [
                {
                    "transaction_id": "tx_103",
                    "amount": 1999,
                    "currency": "USD",
                    "customer_email": "customer3@example.com",
                    "status": "Failed",
                    "created_at": "2026-09-09T12:00:00Z"
                }
            ]
        }

#---------------------------------------------------------
#MAIN EXTRACTOR FUNCTION
#---------------------------------------------------------
            
def extract_stripe():
    """
    Extract, validate and store a Stripe payment.
    """
    
    print("Starting Stripe extraction...")
    print(f"Stripe API URL: {STRIPE_API_URL}")

    all_validated_payments = []
    has_more = True
    starting_after = None
    page_count = 1


   #---------------------------------------------------------
   #CURSORE PAGIONATION LOOP
    #---------------------------------------------------------

    while has_more:
        print (f"Fetching Stripe Batch Page {page_count} (starting_after: {starting_after})...")

        #1. FETCH CURRENT APUI PAGE 
        response = fetch_strip_page(starting_after=starting_after)
        records = response.get("data", [])
        # 2. Schema Validation via Pydantic Model
        for raw_item in records:
            payment = StripePaymentSchema(**raw_item)
            validated_data = payment.model_dump(mode="json")
            all_validated_payments.append(validated_data)

        # 3. Update Cursor Control Variables
        has_more = response.get("has_more", False)
        if records:
            # Set cursor pointer to the last transaction's ID
            starting_after = records[-1]["transaction_id"]

        page_count += 1
        time.sleep(0.5)  # Simulated API rate limit delay

    print(f"Successfully validated {len(all_validated_payments)} payments across all pages.")

    # ---------------------------------------------------------
    # Save Consolidated Dataset to Bronze Layer
    # ---------------------------------------------------------
    filename = "stripe_payments_originted.json"
    save_to_local_lake(
        data=validated_data,
        source="stripe",
        filename=filename
    )

    print("Stripe extraction completed successfully.")


# Module execution block
if __name__ == "__main__":
    extract_stripe()  