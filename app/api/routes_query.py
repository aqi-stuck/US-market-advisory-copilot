import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import QueryRequest, QueryResponse
from app.core.security import get_api_key
from app.db.models import QueryLog
from app.db.session import get_db
from app.rag.pipeline import run_pipeline

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    start = time.perf_counter()

    answer, chunks, retrieved_k, reranked_k = run_pipeline(
        query=request.query,
        top_k=request.top_k or 8,
        rerank_k=3,
        lane_hint=request.lane_hint,
    )

    citations = []
    if request.include_citations and chunks:
        citations = [
            {
                "source_title": item.get("title") or "Unknown source",
                "source_url": item.get("source_url") or "",
                "chunk_id": str(item.get("chunk_id") or ""),
                "quote": (item.get("chunk_text") or "")[:280],
            }
            for item in chunks
        ]

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    log = QueryLog(
        question=request.query,
        answer=answer,
        lane_hint=request.lane_hint,
        retrieval_k=retrieved_k,
        reranked_k=reranked_k,
        latency_ms=latency_ms,
        extra_metadata={"stage": "full_pipeline"},
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return QueryResponse(
        answer=answer,
        citations=citations,
        metadata={
            "retrieval_k": retrieved_k,
            "reranked_k": reranked_k,
            "latency_ms": latency_ms,
            "query_log_id": log.id,
        },
    )
