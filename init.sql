
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    source_url VARCHAR(500),
    title VARCHAR(255) NOT NULL,
    lane VARCHAR(50) NOT NULL,
    published_at TIMESTAMP,
    raw_text TEXT,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    qdrant_point_id VARCHAR(100),
    embedding_model VARCHAR(100),
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT,
    lane_hint VARCHAR(50),
    retrieval_k INTEGER NOT NULL DEFAULT 0,
    reranked_k INTEGER NOT NULL DEFAULT 0,
    latency_ms DOUBLE PRECISION,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    id SERIAL PRIMARY KEY,
    lane VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    source_count INTEGER NOT NULL DEFAULT 0,
    chunk_count INTEGER NOT NULL DEFAULT 0,
    details JSONB,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMP
);
