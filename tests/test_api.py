import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from main import app

client = TestClient(app)

class TestChatAPI:
    """Test cases for chat API endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
    
    @patch('app.api.endpoints.chat.get_llm')
    @patch('app.api.endpoints.chat.get_vector_store')
    @patch('app.api.endpoints.chat.get_chains')
    def test_query_chat_success(self, mock_chains, mock_vector_store, mock_llm):
        """Test successful chat query processing."""
        # Mock the chains
        mock_chain = MagicMock()
        mock_chain.run.return_value = '{"intent": "career_guidance", "confidence": 0.9}'
        mock_chains.return_value = {
            'intent': mock_chain,
            'career': MagicMock(run=lambda x: "Career advice response")
        }
        
        # Mock vector store
        mock_vector_store.return_value = None
        
        # Test data
        test_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "What career advice do you have?"
        }
        
        response = client.post("/api/chat/query", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "intent" in data
        assert "confidence" in data
        assert "response_time_ms" in data
    
    def test_query_chat_invalid_input(self):
        """Test chat query with invalid input."""
        # Test empty query
        test_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": ""
        }
        response = client.post("/api/chat/query", json=test_data)
        assert response.status_code == 422  # Validation error
    
    def test_query_chat_missing_fields(self):
        """Test chat query with missing required fields."""
        test_data = {
            "user_id": "test_user",
            "query": "Test query"
        }
        response = client.post("/api/chat/query", json=test_data)
        assert response.status_code == 422  # Validation error
    
    @patch('app.api.endpoints.chat.get_chat_history')
    def test_get_chat_history(self, mock_history):
        """Test getting chat history."""
        mock_history.return_value = [
            {"query": "Test query", "answer": "Test answer", "created_at": "2024-01-01"}
        ]
        
        response = client.get("/api/chat/history/test_user/test_session")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert "total_count" in data
        assert "session_id" in data
        assert data["session_id"] == "test_session"
    
    @patch('app.api.endpoints.chat.get_chat_history')
    def test_get_chat_history_with_limit(self, mock_history):
        """Test getting chat history with limit parameter."""
        mock_history.return_value = []
        
        response = client.get("/api/chat/history/test_user/test_session?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 0

class TestDatabase:
    """Test cases for database operations."""
    
    @patch('app.core.database.get_connection_pool')
    def test_create_tables(self, mock_pool):
        """Test database table creation."""
        from app.core.database import create_tables
        
        # Mock the connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.return_value.getconn.return_value = mock_conn
        
        # This should not raise an exception
        create_tables()
        assert mock_cursor.execute.called
    
    @patch('app.core.database.get_connection_pool')
    def test_log_chat(self, mock_pool):
        """Test chat logging."""
        from app.core.database import log_chat
        
        # Mock the connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pool.return_value.getconn.return_value = mock_conn
        
        # This should not raise an exception
        log_chat("test_user", "test_session", "test query", "test answer")
        assert mock_cursor.execute.called

class TestVectorStore:
    """Test cases for vector store operations."""
    
    @patch('app.core.vectorstore.pinecone')
    @patch('app.core.vectorstore.OpenAIEmbeddings')
    def test_create_vector_store_success(self, mock_embeddings, mock_pinecone):
        """Test successful vector store creation."""
        from app.core.vectorstore import create_vector_store
        
        # Mock the components
        mock_pinecone.Pinecone.return_value = MagicMock()
        mock_embeddings.return_value = MagicMock()
        
        # Mock settings
        with patch('app.core.vectorstore.settings') as mock_settings:
            mock_settings.PINECONE_API_KEY = "test_key"
            mock_settings.PINECONE_ENV = "test_env"
            mock_settings.OPENAI_API_EMBEDDING_MODEL = "text-embedding-3-small"
            mock_settings.OPENAI_API_KEY = "test_openai_key"
            mock_settings.PINECONE_INDEX = "test_index"
            mock_settings.PINECONE_NAMESPACE = "test_namespace"
            
            result = create_vector_store()
            assert result is not None
    
    @patch('app.core.vectorstore.pinecone')
    def test_create_vector_store_failure(self, mock_pinecone):
        """Test vector store creation failure."""
        from app.core.vectorstore import create_vector_store
        
        # Mock failure
        mock_pinecone.Pinecone.side_effect = Exception("Connection failed")
        
        result = create_vector_store()
        assert result is None

class TestConfig:
    """Test cases for configuration."""
    
    def test_settings_loading(self):
        """Test that settings can be loaded."""
        from app.core.config import settings
        
        # Check that settings object exists
        assert settings is not None
        assert hasattr(settings, 'OPENAI_API_KEY')
        assert hasattr(settings, 'OPENAI_MODEL_NAME')

if __name__ == "__main__":
    pytest.main([__file__])
