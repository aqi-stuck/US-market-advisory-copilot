# Development Dockerfile for Pakistan Market Advisory RAG System
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry==1.7.1 poetry-plugin-export

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies (poetry will generate lock file if needed)
RUN poetry config virtualenvs.create false \
    && poetry lock --no-update 2>/dev/null || true \
    && poetry install --no-interaction --no-root

# Copy application code
COPY . .

# Install the project itself
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
