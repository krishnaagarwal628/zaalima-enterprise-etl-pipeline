import os
import time
from dotenv import load_dotenv

from models.schemas import SalesforceLeadSchema
from data_lake.storage import save_to_local_lake


# Load environment variables
load_dotenv()

SALESFORCE_API_URL = os.getenv("SALESFORCE_API_URL")



def fetch_salesforce_soql_page (next_records_url= None):
    """
    Simulates Salesforce SOQL Query Pagination API.
    Returns records, 'done' boolean status, and 'nextRecordsUrl'.
    """
    if not next_records_url:
        #page 1 Response 
        return{
            "totalSize": 3,
            "done": False,
            "nextRecordsUrl": "/services/data/v57.0/query/01gD0000002HU6i-200",
            "records": [
                {
                    "lead_id": "lead_001",
                    "first_name": "John",
                    "last_name": "Doe",
                    "company": "ABC Tech",
                    "email": "john.doe@example.com",
                    "phone": "+919876543210",
                    "created_date": "2026-09-09"
                },
                {
                    "lead_id": "lead_002",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "company": "XYZ Corp",
                    "email": "jane.smith@example.com",
                    "phone": "+919876543211",
                    "created_date": "2026-09-09"
                }
            ]
        }
    else:
        #page 2 Response (Final Page )
        return{
            "totalSize": 3,
            "done": True,
            "nextRecordsUrl": None,
            "records": [
                {
                    "lead_id": "lead_003",
                    "first_name": "Alice",
                    "last_name": "Taylor",
                    "company": "Global Solution",
                    "email": "alex.t@example.com",
                    "phone": "+919876543212",
                    "created_date": "2026-09-09"
                }
            ]
        }



def extract_salesforce():
    """
    Extract, validate and store a Salesforce lead,with SOQL Pagination.
    """

    print("Starting Salesforce extraction with SOQL pagination...")
    print(f"Salesforce API URL: {SALESFORCE_API_URL}")

    all_validated_leads = []
    done = False
    next_records_url = None
    page_count = 1
    
    # ---------------------------------------------------------
    # Pagination Loop Execution
    # ---------------------------------------------------------
    while not done:
        print(f"Fetching Salesforce SOQL Page {page_count}...")
        
        # 1. Fetch Batch Data
        response = fetch_salesforce_soql_page(next_records_url=next_records_url)
        raw_records = response.get("records", [])
        
        # 2. Schema Validation via Pydantic
        for raw_item in raw_records:
            lead = SalesforceLeadSchema(**raw_item)
            validated_data = lead.model_dump(mode="json")
            all_validated_leads.append(validated_data)
        
        # 3. Update Pagination Controls
        done = response.get("done", True)
        next_records_url = response.get("nextRecordsUrl")
        page_count += 1
        time.sleep(0.5)  # Rate limiting delay simulation

    print(f"Successfully validated {len(all_validated_leads)} leads across all pages.")

    # ---------------------------------------------------------
    # Save Consolidated Dataset to Bronze Layer
    # ---------------------------------------------------------
    filename = "salesforce_leads_paginated.json"
    save_to_local_lake(
        data=all_validated_leads,
        source="salesforce",
        filename=filename
    )

    print("Salesforce extraction completed successfully.")

if __name__ == "__main__":
    extract_salesforce()  # <--- Is line ke aage 4 spaces ya 1 Tab zaroor dein!