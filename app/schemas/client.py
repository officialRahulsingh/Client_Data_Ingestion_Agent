from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class ClientResponse(BaseModel):
    id: int
    client_code: str
    client_name: str
    email: str
    phone: str
    city: str
    state: str
    status: str
    revenue: float
    created_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IngestionResponse(BaseModel):
    message: str
    rows_read: int
    rows_inserted: int
    chunk_size: int
    chunks_processed: int


class ChunkResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int
    data: list[ClientResponse]


class HealthResponse(BaseModel):
    status: str
    database: str
