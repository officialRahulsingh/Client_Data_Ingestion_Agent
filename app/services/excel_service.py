from io import BytesIO
from typing import BinaryIO
import pandas as pd


REQUIRED_COLUMNS = [
    "client_code",
    "client_name",
    "email",
    "phone",
    "city",
    "state",
    "status",
    "revenue",
    "created_date",
]


def read_and_clean_excel(file: BinaryIO) -> pd.DataFrame:
    content = file.read()
    if not content:
        raise ValueError("Uploaded Excel file is empty.")

    try:
        df = pd.read_excel(BytesIO(content), engine="openpyxl")
    except Exception as exc:
        raise ValueError(f"Could not read Excel file: {exc}") from exc

    if df.empty:
        raise ValueError("Excel file does not contain any data rows.")

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required Excel columns: {', '.join(missing)}")

    df = df[REQUIRED_COLUMNS].copy()

    text_columns = [
        "client_code", "client_name", "email", "phone",
        "city", "state", "status"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    df["email"] = df["email"].str.lower()
    df["status"] = df["status"].str.lower()
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)
    df["created_date"] = pd.to_datetime(
        df["created_date"], errors="coerce"
    ).dt.date

    df = df.dropna(subset=["created_date"])
    df = df[df["client_code"] != ""]
    df = df.drop_duplicates(subset=["client_code"], keep="last")

    if df.empty:
        raise ValueError("No valid rows remained after cleaning.")

    return df
