from datetime import date
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.client import Client
from app.schemas.client import ChunkResponse, ClientResponse, IngestionResponse
from app.services.excel_service import read_and_clean_excel
from app.services.filter_service import fetch_filtered_clients
from app.services.ingestion_service import insert_dataframe_in_chunks

router = APIRouter(prefix="/api/v1/clients", tags=["Clients"])


@router.post("/ingest", response_model=IngestionResponse)
def ingest_excel(
    file: UploadFile = File(..., description="Excel .xlsx file"),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Please upload an Excel .xlsx file.")

    try:
        df = read_and_clean_excel(file.file)
        inserted, chunks = insert_dataframe_in_chunks(
            db=db,
            df=df,
            chunk_size=settings.insert_chunk_size,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Data ingestion failed: {exc}") from exc

    return IngestionResponse(
        message="Client data ingested successfully",
        rows_read=len(df),
        rows_inserted=inserted,
        chunk_size=settings.insert_chunk_size,
        chunks_processed=chunks,
    )


@router.get("", response_model=list[ClientResponse])
def get_all_clients(db: Session = Depends(get_db)):
    return list(db.scalars(select(Client).order_by(Client.id)).all())


@router.get("/chunks", response_model=ChunkResponse)
def get_clients_in_chunks(
    chunk_size: int | None = Query(default=None, ge=1, le=1000),
    chunk_number: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    size = chunk_size or settings.fetch_chunk_size
    total = db.scalar(select(func.count()).select_from(Client)) or 0
    total_pages = max(1, (total + size - 1) // size)

    if total == 0:
        return ChunkResponse(
            page=chunk_number, page_size=size, total_records=0,
            total_pages=0, data=[]
        )

    if chunk_number > total_pages:
        raise HTTPException(
            status_code=404,
            detail=f"chunk_number must be between 1 and {total_pages}",
        )

    rows = list(
        db.scalars(
            select(Client)
            .order_by(Client.id)
            .offset((chunk_number - 1) * size)
            .limit(size)
        ).all()
    )

    return ChunkResponse(
        page=chunk_number,
        page_size=size,
        total_records=total,
        total_pages=total_pages,
        data=rows,
    )


@router.get("/filter", response_model=list[ClientResponse])
def filter_clients(
    city: str | None = None,
    state: str | None = None,
    status: str | None = None,
    client_name: str | None = None,
    email: str | None = None,
    client_code: str | None = None,
    min_revenue: float | None = Query(default=None, ge=0),
    max_revenue: float | None = Query(default=None, ge=0),
    created_from: date | None = None,
    created_to: date | None = None,
    db: Session = Depends(get_db),
):
    if min_revenue is not None and max_revenue is not None and min_revenue > max_revenue:
        raise HTTPException(status_code=400, detail="min_revenue cannot be greater than max_revenue")

    if created_from and created_to and created_from > created_to:
        raise HTTPException(status_code=400, detail="created_from cannot be later than created_to")

    rows, _ = fetch_filtered_clients(
        db,
        city=city,
        state=state,
        status=status,
        client_name=client_name,
        email=email,
        client_code=client_code,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        created_from=created_from,
        created_to=created_to,
    )

    return rows
