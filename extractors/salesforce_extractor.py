import os

from dotenv import load_dotenv

from models.schemas import SalesforceLeadSchema
from data_lake.storage import save_to_local_lake


# Load environment variables
load_dotenv()

SALESFORCE_API_URL = os.getenv(
    "SALESFORCE_API_URL"
)


def extract_salesforce():
    """
    Extract, validate and store a Salesforce lead.
    """
    load_dotenv()

    SALESFORCE_API_URL = os.getenv(
    "SALESFORCE_API_URL"
)
    print("Starting Salesforce extraction...")
    print(
        f"Salesforce API URL: {SALESFORCE_API_URL}"
    )

    # ---------------------------------------------------------
    # Simulated raw Salesforce lead
    # ---------------------------------------------------------

    raw_payload = {
        "lead_id": "lead_001",
        "first_name": "John",
        "last_name": "Doe",
        "company": "ABC Technologies",
        "email": "john.doe@example.com",
        "phone": "+919876543210",
        "created_date": "2026-09-09"
    }

    print(
        "Salesforce raw payload received."
    )

    # ---------------------------------------------------------
    # Validate using Pydantic
    # ---------------------------------------------------------

    lead = SalesforceLeadSchema(
        **raw_payload
    )

    print(
        "Salesforce payload validation successful."
    )

    # ---------------------------------------------------------
    # Convert validated model to JSON-compatible dictionary
    # ---------------------------------------------------------

    validated_data = lead.model_dump(
        mode="json"
    )
    filename = f"salesforce_{lead.lead_id}.json"
    # ---------------------------------------------------------
    # Save to Bronze layer
    # ---------------------------------------------------------

    save_to_local_lake(
        data=validated_data,
        source="salesforce",
        filename=filename
    )

    print(
        "Salesforce extraction completed successfully."
    )