from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import requests

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    details: Optional[dict] = None


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service availability
    """
    db_status = "ok"
    vectorstore_status = "ok"

    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"

    try:
        response = requests.get(f"{settings.QDRANT_URL}/health", timeout=3)
        response.raise_for_status()
    except requests.RequestException:
        vectorstore_status = "error"

    details = {
        "database": db_status,
        "vectorstore": vectorstore_status,
    }

    status = "ok" if db_status == "ok" and vectorstore_status == "ok" else "degraded"

    return HealthResponse(status=status, version=settings.VERSION, details=details)
