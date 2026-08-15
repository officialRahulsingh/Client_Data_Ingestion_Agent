from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.models.client import Client
from app.routes.clients import router as clients_router
from app.routes.health import router as health_router

_ = Client


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Excel -> Pandas -> FastAPI -> MySQL client data ingestion API.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(clients_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": settings.app_name,
        "docs": "/docs",
        "health": "/health",
    }
