# Enterprise ETL Pipeline & Data Warehouse Synchronizer

## Overview
Resilient, automated Data Engineering pipeline designed to extract business data from third-party APIs (Salesforce, Stripe), transform schemas, and load securely into a central Data Warehouse.

## Tech Stack
Python 3.11+, Pydantic, Requests, Tenacity, AWS S3, Apache Airflow, PostgreSQL


# 🚀 Zaalima Enterprise ETL Pipeline

A scalable, modular data pipeline built in Python following the **Medallion Architecture** pattern. This project ingests raw transactional and lead data from multi-source systems (Stripe & Salesforce), validates payload integrity using Pydantic schemas, and lands raw records into a structured Bronze Data Lake layer.

---

## 🏗 Architecture Overview

```text
┌───────────────────┐      ┌─────────────────────────┐      ┌──────────────────────────────────┐
│   Data Sources    │ ───► │  Validation & Ingestion │ ───► │   Data Lake (Bronze/Raw Layer)   │
│ Stripe / Salesforce│      │    Pydantic Schemas     │      │   data_lake/raw/stripe/*.json    │
└───────────────────┘      └─────────────────────────┘      │   data_lake/raw/salesforce/*.json│
                                                              └──────────────────────────────────┘

Bronze Layer (Raw): Ingests raw source payloads as partition-ready JSON files.

Data Validation: Strict schema enforcement via pydantic to ensure clean upstream ingestion.

Configuration & Security: Environment variables isolated via python-dotenv

zaalima-etl-pipeline/
├── data_lake/             # Local Data Lake storage
│   ├── raw/               # Raw JSON outputs (Git ignored)
│   ├── __init__.py
│   └── storage.py         # File persistence handler
├── extractors/            # Source ingestion modules
│   ├── __init__.py
│   ├── salesforce_extractor.py
│   └── stripe_extractor.py
├── models/                # Schema definitions
│   ├── __init__.py
│   └── schemas.py         # Pydantic payment & lead schemas
├── .env.example           # Environment variable templates
├── .gitignore             # Secrets & environment ignore rules
├── main.py                # Pipeline orchestrator & entry point
└── README.md              # Project documentation

git clone [https://github.com/your-username/zaalima-etl-pipeline.git](https://github.com/your-username/zaalima-etl-pipeline.git)
cd zaalima-etl-pipeline

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

pip install python-dotenv pydantic requests tenacity email-validator

ENVIRONMENT=local
STRIPE_API_URL=[https://api.stripe.com/v1/payment_intents](https://api.stripe.com/v1/payment_intents)
SALESFORCE_API_URL=[https://your-instance.salesforce.com/services/data/v58.0/sobjects/Lead](https://your-instance.salesforce.com/services/data/v58.0/sobjects/Lead)

python main.py

============================================================
ZAALIMA ETL PIPELINE - DAY 2
Ingestion Pipeline Started
============================================================

[1/2] Running Stripe extractor...
Starting Stripe extraction...
Stripe API URL: [https://api.stripe.com/v1/payment_intents](https://api.stripe.com/v1/payment_intents)
Stripe raw payload received.
Stripe payload validation successful.
Saved raw data: data_lake/raw/stripe/stripe_tx_101.json
Stripe extraction: SUCCESS

[2/2] Running Salesforce extractor...
Starting Salesforce extraction...
Salesforce API URL: [https://your-instance.salesforce.com/services/data/v58.0/sobjects/Lead](https://your-instance.salesforce.com/services/data/v58.0/sobjects/Lead)
Salesforce raw payload received.
Salesforce payload validation successful.
Saved raw data: data_lake/raw/salesforce/salesforce_lead_001.json
Salesforce extraction: SUCCESS

============================================================
Ingestion Pipeline Completed
============================================================

### 📅 Daily Progress Log

#### Week 1 - Day 3: Architecture Planning & API Mechanics Study
- **Technical Research:** Studied Stripe cursor-based pagination (`starting_after`, `has_more`) and Salesforce REST/SOQL pagination mechanisms (`nextRecordsUrl`, `done` flag)[cite: 1].
- **Pipeline Preparation:** Finalized data extraction flow and Pydantic validation mapping strategies for Day 4 implementation[cite: 1].
- **Team Sync:** Documented API specs and modular file structure for upcoming extraction scripts[cite: 1].

#### Week 1 - Days 4 & 5: SOQL & Cursor Pagination Implementation
- **Salesforce Pagination:** Implemented SOQL query pagination handling using dynamic `nextRecordsUrl` tracking and `done` flag evaluation to extract full lead batches.
- **Stripe Pagination:** Added cursor-based pagination loop utilizing `starting_after` parameters and `has_more` status checks.
- **Data Lake Storage:** Updated extraction modules (`salesforce_extractor.py`, `stripe_extractor.py`) to consolidate validated multi-page records into JSON output files within `data_lake/raw/`.

#### Week 1 - Days 6 & 7: Centralized Pipeline Orchestration & Week 1 Wrap-up
- **Pipeline Orchestrator (`main.py`):** Integrated `stripe_extractor` and `salesforce_extractor` into a single entry-point execution flow with dynamic error handling and module logging.
- **End-to-End Extraction Verification:** Successfully validated multi-source ingestion, schema enforcement, and Bronze Data Lake persistence across Stripe and Salesforce modules.
- **Repository Optimization:** Untracked virtual environments, standardized directory structures, and verified environment configuration for production readiness.


#### Week 2 - Days 1 to 3: Silver Layer Transformations & Standardizations
- **Data Cleaning & Null Handling:** Built dedicated Pandas transformation scripts (`stripe_transformer.py`, `salesforce_transformer.py`) to handle missing values and filter invalid records.
- **Format Normalization:** Standardized raw date strings into standard ISO 8601 timestamps and normalized multi-currency transaction values into decimal floats.
- **Silver Persistence:** Landed processed, cleaned payloads into partitioned Silver Data Lake storage (`data_lake/silver/`).

#### Week 2 - Days 4 & 5: Batch Processing & Central Pipeline Orchestration
- **Dynamic Directory Scanning:** Added dynamic batch scanners (`batch_transform_stripe_dir`, `batch_transform_salesforce_dir`) to auto-discover and transform all raw JSON files in batch.
- **Full Pipeline Orchestration:** Upgraded `main.py` to seamlessly orchestrate end-to-end processing across both Bronze (Raw Ingestion) and Silver (Transformation) layers.

#### Week 2 - Days 6 & 7: Unified Schema Mapping & Pytest Validation
- **Common Data Model (Unified Schema):** Built `unified_transformer.py` to map disparate source entities (Stripe `charge_id` / Salesforce `opportunity_id`) into a single standardized transaction model (`unified_silver.json`).
- **Pytest Integration:** Created automated unit test suites (`tests/test_transformers.py`) to validate schema conversions, data types, and transformation integrity across modules.
- **Week 2 Milestone Completion:** Verified full pipeline execution, green Pytest test suite, and merged tested codebase into `main`.