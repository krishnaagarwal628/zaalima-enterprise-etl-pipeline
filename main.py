from extractors.stripe_extractor import extract_stripe
from extractors.salesforce_extractor import extract_salesforce


def main():

    print("=" * 60)
    print("ZAALIMA ETL PIPELINE - WEEK 1 COMPLETE")
    print("Ingestion Pipeline Started")
    print("=" * 60)

    # ---------------------------------------------------------
    # Stripe
    # ---------------------------------------------------------

    print("\n[1/2] Running Stripe extractor...")

    try:
        extract_stripe()
        print("Stripe extraction: SUCCESS")

    except Exception as error:
        print(f"Stripe extraction: FAILED - {error}")

    # ---------------------------------------------------------
    # Salesforce
    # ---------------------------------------------------------

    print("\n[2/2] Running Salesforce extractor...")

    try:
        extract_salesforce()
        print("Salesforce extraction: SUCCESS")

    except Exception as error:
        print(
            f"Salesforce extraction: FAILED - {error}"
        )

    # ---------------------------------------------------------
    # Pipeline completed
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("Ingestion Pipeline Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()