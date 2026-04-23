import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import QueryRequest, QueryResponse
from app.core.security import get_api_key
from app.db.models import QueryLog
from app.db.session import get_db

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    """
    Main query endpoint for the RAG system.
    Current milestone: return placeholder answer and persist query log.
    """
    start = time.perf_counter()

    answer = (
        f"This is a placeholder response for query: '{request.query}'. "
        "Next step will connect retrieval and generation pipeline."
    )

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    log = QueryLog(
        question=request.query,
        answer=answer,
        lane_hint=request.lane_hint,
        retrieval_k=0,
        reranked_k=0,
        latency_ms=latency_ms,
        extra_metadata={"stage": "placeholder"},
    )
    db.add(log)
    db.commit()

    return QueryResponse(
        answer=answer,
        citations=[],
        metadata={
            "retrieval_k": 0,
            "reranked_k": 0,
            "latency_ms": latency_ms,
            "query_log_id": log.id,
        },
    )
