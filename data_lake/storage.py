import os
import json


def save_to_local_lake(data: dict, source: str, filename: str):
    """
    Save validated data into the local Bronze/raw data lake.

    Location:
        data_lake/raw/{source}/{filename}
    """

    folder_path = os.path.join(
        "data_lake",
        "raw",
        source
    )

    # Create folder automatically if it doesn't exist
    os.makedirs(
        folder_path,
        exist_ok=True
    )

    file_path = os.path.join(
        folder_path,
        filename
    )

    # Write JSON with indentation for readability
    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved raw data: {file_path}")

    return file_path