# Multi-stage Dockerfile for Pakistan Market Advisory RAG System

# Build stage
FROM python:3.11-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry==1.7.1

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml ./

# Install dependencies
RUN poetry export -o requirements.txt -f requirements.txt --without-hashes
RUN pip install --user --no-cache-dir -r requirements.txt
# Production stage
FROM python:3.11-slim AS production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local/share/pypoetry /root/.local/share/pypoetry
COPY --from=builder /root/.local/bin /root/.local/bin

# Add poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]