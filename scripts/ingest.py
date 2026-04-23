import json
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.data.preprocess.chunking import chunk_text
from app.db.models import Chunk, Document, IngestionRun
from app.db.session import SessionLocal


def parse_datetime(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_file = project_root / "data" / "raw" / "seed_market_docs.json"

    if not input_file.exists():
        raise FileNotFoundError(f"Missing input file: {input_file}")

    with input_file.open("r", encoding="utf-8") as f:
        records = json.load(f)

    db = SessionLocal()
    run = IngestionRun(
        lane="mixed",
        status="running",
        source_count=len(records),
        chunk_count=0,
        details={"source_file": str(input_file)},
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    total_chunks = 0

    try:
        for row in records:
            doc = Document(
                source_name=row.get("source_name", "unknown"),
                source_url=row.get("source_url"),
                title=row.get("title", "untitled"),
                lane=row.get("lane", "macro"),
                published_at=parse_datetime(row.get("published_at")),
                raw_text=row.get("raw_text", ""),
                extra_metadata={"ingestion_run_id": run.id},
            )
            db.add(doc)
            db.flush()

            chunks = chunk_text(
                doc.raw_text or "",
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
            )

            for idx, text_part in enumerate(chunks):
                db.add(
                    Chunk(
                        document_id=doc.id,
                        chunk_index=idx,
                        chunk_text=text_part,
                        qdrant_point_id=None,
                        embedding_model=None,
                        extra_metadata={"lane": doc.lane},
                    )
                )

            total_chunks += len(chunks)

        run.status = "completed"
        run.chunk_count = total_chunks
        db.commit()
        print(f"Ingestion complete. documents={len(records)} chunks={total_chunks}")

    except Exception as exc:
        run.status = "failed"
        run.details = {"error": str(exc)}
        db.commit()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()