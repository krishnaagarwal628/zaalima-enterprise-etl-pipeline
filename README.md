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

#### Week 1 - Days 4 & 5: Stripe & Salesforce Pagination & Schema Validation
- **Stripe Cursor Pagination:** Implemented cursor-based pagination loop utilizing `starting_after` parameter tracking and `has_more` boolean evaluations to extract full multi-page payment intent batches.
- **Salesforce SOQL Pagination:** Built offset/SOQL-style pagination handling via dynamic `nextRecordsUrl` tracking and `done` flag assertion for complete lead extraction.
- **Pydantic Schema Enforcement:** Integrated strict runtime validation using `StripePaymentSchema` and `SalesforceLeadSchema` before persisting records upstream.
- **Bronze Lake Persistence:** Updated extraction outputs to consolidate validated multi-page batches into structured JSON datasets (`stripe_payments_paginated.json` & `salesforce_leads_paginated.json`) inside `data_lake/raw/`.