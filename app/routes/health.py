from fastapi import APIRouter
from app.database import check_database_connection
from app.schemas.client import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    database_ok = check_database_connection()
    return {
        "status": "healthy" if database_ok else "unhealthy",
        "database": "connected" if database_ok else "not connected",
    }
