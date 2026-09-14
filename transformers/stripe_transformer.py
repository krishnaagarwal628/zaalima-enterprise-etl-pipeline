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


