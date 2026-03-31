# Pakistan Market Advisory RAG System

A Retrieval-Augmented Generation (RAG) system designed to provide insights on Pakistani financial markets, including stock trends (PSX), macroeconomic indicators (GDP, inflation), and financial regulations.

## Overview

This system provides a comprehensive platform for analyzing and understanding Pakistan's financial landscape through:
- Real-time stock market data and trends from PSX
- Macroeconomic indicators from PBS, SBP, and World Bank
- Financial regulations and circulars from SECP, SBP, and PSX

## Architecture

The system follows a modular architecture:

```
market-advisory-rag/
├─ README.md
├─ .gitignore
├─ .env.example
├─ docker-compose.yml
├─ Dockerfile
├─ pyproject.toml                 # or requirements.txt
├─ Makefile                       # common dev commands
├─ scripts/
│  ├─ bootstrap.sh                # one-command setup
│  ├─ download_data.py            # pulls raw datasets (APIs/CSV/PDF)
│  ├─ ingest.py                   # runs chunk → embed → upsert
│  ├─ eval_rag.py                 # offline evaluation
│  └─ backfill_metadata.py        # optional repair jobs
├─ data/
│  ├─ raw/                        # PDFs, CSVs, HTML snapshots
│  ├─ interim/                    # cleaned, normalized artifacts
│  └─ processed/                  # chunks (jsonl), embeddings manifest
├─ notebooks/
│  ├─ 01_explore_sources.ipynb
│  ├─ 02_chunking_experiments.ipynb
│  └─ 03_retrieval_quality.ipynb
├─ app/
│  ├─ main.py                     # FastAPI entrypoint
│  ├─ core/
│  │  ├─ config.py                # settings, env vars
│  │  ├─ logging.py               # structured logging
│  │  ├─ security.py              # API key/JWT helpers
│  │  └─ exceptions.py            # unified error types
│  ├─ api/
│  │  ├─ routes_health.py
│  │  ├─ routes_query.py
│  │  ├─ routes_ingest.py         # optional protected endpoints
│  │  └─ schemas.py               # Pydantic request/response models
│  ├─ rag/
│  │  ├─ pipeline.py              # orchestrates retrieve → generate
│  │  ├─ retriever.py             # vector + filters + hybrid (optional)
│  │  ├─ reranker.py              # optional cross-encoder rerank
│  │  ├─ prompt.py                # prompt templates
│  │  ├─ citations.py             # quote spans + source formatting
│  │  └─ guardrails.py            # refusal rules, scope checks
│  ├─ data/
│  │  ├─ sources.py               # source registry (PSX/SBP/SECP/…)
│  │  ├─ loaders/
│  │  │  ├─ pdf_loader.py
│  │  │  ├─ csv_loader.py
│  │  │  └─ web_loader.py
│  │  ├─ preprocess/
│  │  │  ├─ clean_text.py
│  │  │  ├─ normalize_tables.py   # GDP/market tables
│  │  │  └─ chunking.py
│  │  └─ metadata.py              # doc_id, section, dates, entity tags
│  ├─ vectorstore/
│  │  ├─ qdrant_client.py
│  │  └─ index.py                 # create collection, upsert, search
│  ├─ llm/
│  │  ├─ client.py                # OpenAI/Anthropic/etc wrapper
│  │  └─ embeddings.py
│  └─ db/
│     ├─ models.py                # SQLAlchemy tables (docs, queries, runs)
│     └─ session.py
├─ tests/
│  ├─ test_api.py
│  ├─ test_chunking.py
│  ├─ test_retrieval.py
│  └─ test_guardrails.py
└─ .github/workflows/
   ├─ ci.yml                      # lint + tests
   └─ cd.yml                      # build + push image (optional)
```

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the required values
3. Run `make setup` or `./scripts/bootstrap.sh`

## Development

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Poetry (for dependency management)

### Running Locally

```bash
# Start the services
docker-compose up -d

# Install dependencies
poetry install

# Run the application
poetry run python -m app.main
```

### API Endpoints

- `GET /health` - Health check endpoint
- `POST /v1/query` - Main query endpoint for RAG system
- `POST /v1/ingest` - Protected ingestion endpoint

## Data Sources

The system integrates three primary data lanes:

### A) Stock Market Trends (PSX)
- Daily prices, volume, index constituents (KSE-100, sector indices)
- Corporate actions and announcements

### B) GDP + Macro Data (PBS, SBP, World Bank)
- GDP (nominal/real), CPI, interest rate, FX reserves, trade balance

### C) Financial Regulations (SECP, SBP, PSX)
- PDFs, circulars, regulations, amendments, dates, applicability

## Contributing

Please read our contributing guidelines before submitting pull requests.