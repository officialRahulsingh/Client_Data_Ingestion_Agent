import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.client import Client


def dataframe_to_records(df: pd.DataFrame) -> list[dict]:
    records = df.to_dict(orient="records")
    for record in records:
        record["revenue"] = float(record["revenue"])
    return records


def insert_dataframe_in_chunks(
    db: Session,
    df: pd.DataFrame,
    chunk_size: int,
) -> tuple[int, int]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    inserted = 0
    chunks_processed = 0

    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        records = dataframe_to_records(chunk)
        codes = [record["client_code"] for record in records]

        existing_codes = set(
            db.scalars(
                select(Client.client_code).where(Client.client_code.in_(codes))
            ).all()
        )

        new_records = [
            record for record in records
            if record["client_code"] not in existing_codes
        ]

        if new_records:
            db.add_all([Client(**record) for record in new_records])
            db.commit()
            inserted += len(new_records)

        chunks_processed += 1

    return inserted, chunks_processed
