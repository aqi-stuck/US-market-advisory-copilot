import os
import sys

# Set test environment BEFORE any imports from app
os.environ["ENVIRONMENT"] = "development"
os.environ["API_KEY"] = "test-api-key-12345"  # Non-empty for auth testing
os.environ["AZURE_OPENAI_API_KEY"] = "test-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://test.openai.azure.com/"

import pytest
from unittest.mock import MagicMock, patch, Mock
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db


def create_mock_db():
    """Create a properly mocked database session."""
    mock_db = MagicMock()
    
    # Mock add() to do nothing (it just tracks calls)
    mock_db.add = MagicMock()
    
    # Mock flush() and commit() to do nothing
    mock_db.flush = MagicMock()
    mock_db.commit = MagicMock()
    
    # Mock refresh() to do nothing but set id on model if needed
    def mock_refresh(obj):
        if hasattr(obj, 'id') and obj.id is None:
            obj.id = 1
    mock_db.refresh = MagicMock(side_effect=mock_refresh)
    
    # Mock query() to return a mock query object
    mock_query = MagicMock()
    mock_query.filter = MagicMock(return_value=MagicMock())
    mock_query.filter.return_value.first = MagicMock(return_value=None)
    mock_db.query = MagicMock(return_value=mock_query)
    
    return mock_db


def override_get_db():
    """Mock database session for testing."""
    yield create_mock_db()


@pytest.fixture
def client():
    """Create test client with mocked dependencies."""
    app.dependency_overrides[get_db] = override_get_db
    
    with patch('app.rag.pipeline.run_pipeline') as mock_pipeline, \
         patch('app.llm.clients.get_chat_client'), \
         patch('app.rag.retriever.retrieve_chunks'), \
         patch('app.vectorstore.qdrant_client.upsert_points'), \
         patch('app.llm.embeddings.embed_text') as mock_embed, \
         patch('app.data.preprocess.chunking.chunk_text') as mock_chunk:
        
        # Mock embeddings to return a list of floats
        mock_embed.return_value = [0.1] * 1536
        
        # Mock chunking to return empty list (for empty documents)
        mock_chunk.return_value = []
        
        # Mock pipeline to return test data
        mock_pipeline.return_value = (
            "Based on current US equity market trends, the S&P 500 shows positive momentum.",
            [
                {
                    "title": "Market Overview",
                    "source_url": "https://example.com",
                    "chunk_id": "1",
                    "chunk_text": "The S&P 500 is up 2.5% this quarter."
                }
            ],
            5,
            3
        )
        
        with TestClient(app) as test_client:
            yield test_client
    
    app.dependency_overrides.clear()
