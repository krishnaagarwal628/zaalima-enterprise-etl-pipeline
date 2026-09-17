import json
from pathlib import Path
import pandas as pd


def load_raw_salesforce_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Raw file not found at: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Invalid JSON format for transformation.")

    return df

def handle_salesforce_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    critical_cols = ["opportunity_id", "account_name"]

    # Ensure critical columns exist in DataFrame before checking nulls
    for col in critical_cols:
        if col not in df_clean.columns:
            df_clean[col] = None

    initial_count = len(df_clean)

    # Missing critical rows drop karna
    df_clean = df_clean.dropna(subset=critical_cols)

    dropped_count = initial_count - len(df_clean)
    if dropped_count > 0:
        print(
            f"[WARNING] Dropped {dropped_count} Salesforce record(s) due to missing critical fields."
        )

    defaults = {
        "stage": "Prospecting",
        "amount": 0.0,
        "probability": 0.0,
    }

    df_clean = df_clean.fillna(value=defaults)

    return df_clean


def deduplicate_salesforce_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    initial_count = len(df_clean)

    df_clean = df_clean.drop_duplicates(subset=["opportunity_id"], keep="last")

    deduped_count = initial_count - len(df_clean)
    if deduped_count > 0:
        print(f"[INFO] Removed {deduped_count} duplicate Salesforce record(s).")

    return df_clean


def clean_salesforce_strings(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    string_cols = df_clean.select_dtypes(include=["object", "string"]).columns

    for col in string_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    return df_clean


def standardize_salesforce_fields(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    if "close_date" in df_clean.columns:
        df_clean["close_date"] = pd.to_datetime(
            df_clean["close_date"], errors="coerce"
        )
        df_clean["close_date"] = df_clean["close_date"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    if "amount" in df_clean.columns:
        df_clean["amount"] = pd.to_numeric(
            df_clean["amount"], errors="coerce"
        ).fillna(0.0)
        df_clean["amount"] = df_clean["amount"].round(2)

    return df_clean


def transform_salesforce_data(
    input_path: str, output_path: str = None
) -> pd.DataFrame:
    """Transforms a single Salesforce JSON file."""
    df = load_raw_salesforce_data(input_path)
    df = handle_salesforce_nulls(df)
    df = deduplicate_salesforce_data(df)
    df = clean_salesforce_strings(df)
    df = standardize_salesforce_fields(df)

    if output_path:
        out_dir = Path(output_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)
        df.to_json(output_path, orient="records", indent=4)
        print(f"[SUCCESS] Saved Silver Salesforce record to: {output_path}")

    return df


def batch_transform_salesforce_dir(
    raw_dir: str = "data_lake/raw/salesforce",
    silver_dir: str = "data_lake/silver/salesforce",
):
    """Dynamically scans raw directory and transforms all Salesforce JSON files."""
    raw_path = Path(raw_dir)
    silver_path = Path(silver_dir)

    if not raw_path.exists():
        print(f"[WARNING] Raw directory {raw_dir} does not exist.")
        return

    json_files = list(raw_path.glob("*.json"))

    if not json_files:
        print(f"[INFO] No JSON files found in {raw_dir}.")
        return

    print(f"[INFO] Found {len(json_files)} raw Salesforce file(s) to process.")

    for file in json_files:
        output_file = silver_path / f"{file.stem}_clean.json"
        transform_salesforce_data(str(file), str(output_file))


