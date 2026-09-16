import json
from pathlib import Path
import pandas as pd


def load_raw_stripe_data(file_path: str) -> pd.DataFrame:
    """Reads a raw Stripe JSON file from Bronze Lake and converts it into a Pandas DataFrame."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Raw file not found at: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Agar JSON single object (dict) hai, toh list mein wrap karke DataFrame banate hain
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Invalid JSON format for transformation.")

    return df



def handle_stripe_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Handles missing and null values in the Stripe DataFrame.

    - Drops rows where critical fields (transaction_id, customer_email) are NaN/Null.
    - Imputes safe defaults for non-critical missing values.
    """
    df_clean = df.copy()

    # 1. Critical Fields Check: Essential fields jin ke bina record invalid hai
    critical_cols = ["transaction_id", "customer_email"]
    initial_count = len(df_clean)

    # Missing critical rows ko drop karein
    df_clean = df_clean.dropna(subset=critical_cols)

    dropped_count = initial_count - len(df_clean)
    if dropped_count > 0:
        print(
            f"[WARNING] Dropped {dropped_count} record(s) due to missing critical fields."
        )

    # 2. Non-Critical Fields Imputation: Safe default values set karein
    defaults = {
        "currency": "USD",
        "status": "pending",
        "amount": 0.0,
    }

    # Jaha NaN ho waha defaults fill karein
    df_clean = df_clean.fillna(value=defaults)

    return df_clean


def deduplicate_stripe_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    initial_count = len(df_clean)

    df_clean = df_clean.drop_duplicates(subset=["transaction_id"], keep="last")

    deduped_count = initial_count - len(df_clean)
    if deduped_count > 0:
        print(f"[INFO] Removed {deduped_count} duplicate record(s).")

    return df_clean



def clean_stripe_strings(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    string_cols = df_clean.select_dtypes(include=["object", "string"]).columns

    for col in string_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    if "customer_email" in df_clean.columns:
        df_clean["customer_email"] = df_clean["customer_email"].str.lower()

    return df_clean





def standardize_stripe_dates(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    if "created_at" in df_clean.columns:
        # datetime string/epoch ko standard datetime object me convert karna
        df_clean["created_at"] = pd.to_datetime(
            df_clean["created_at"], errors="coerce"
        )
        # Standard string format YYYY-MM-DD HH:MM:SS format output
        df_clean["created_at"] = df_clean["created_at"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    return df_clean





def standardize_stripe_currency(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    if "currency" in df_clean.columns:
        df_clean["currency"] = df_clean["currency"].astype(str).str.upper()

    if "amount" in df_clean.columns:
        df_clean["amount"] = pd.to_numeric(
            df_clean["amount"], errors="coerce"
        ).fillna(0.0)
        df_clean["amount"] = df_clean["amount"].round(2)

    return df_clean





def transform_stripe_data(
    input_path: str, output_path: str = None
) -> pd.DataFrame:
    df = load_raw_stripe_data(input_path)
    df = handle_stripe_nulls(df)
    df = deduplicate_stripe_data(df)
    df = clean_stripe_strings(df)
    df = standardize_stripe_dates(df)
    df = standardize_stripe_currency(df)

    if output_path:
        # Silver Layer storage directory check & create
        out_dir = Path(output_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)

        # Transformed clean JSON file write karna
        df.to_json(output_path, orient="records", indent=4)
        print(f"[SUCCESS] Transformed Silver data saved to: {output_path}")

    return df

if __name__ == "__main__":
    raw_path = "data_lake/raw/stripe/stripe_tx_101.json"
    silver_path = "data_lake/silver/stripe/stripe_tx_101_clean.json"

    cleaned_df = transform_stripe_data(raw_path, output_path=silver_path)
    print("--- Transformed Data Output ---")
    print(cleaned_df)