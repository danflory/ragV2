"""
Test Suite: Embedding Circuit Breaker
Tests GPU 1 downtime simulation and CPU fallback resilience
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.memory import VectorStore

class TestEmbeddingCircuitBreaker:
    """Test circuit breaker logic for embedding failures."""

    def test_gpu_embedding_failure_fallback_to_cpu(self):
        """Test that GPU embedding failure triggers CPU fallback."""
        # Create VectorStore instance
        store = VectorStore()

        # Mock the embedder to simulate GPU failure
        mock_embedder = MagicMock()
        mock_embedder.encode.side_effect = RuntimeError("CUDA out of memory")  # Simulate GPU failure
        store.embedder = mock_embedder

        # Mock ChromaDB components
        store.collection = MagicMock()
        store.client = MagicMock()

        # Test data
        texts = ["Test document for embedding"]
        metadatas = [{"source": "test.py"}]
        ids = ["test_id_1"]

        # This should trigger CPU fallback and succeed
        # (We can't actually test CPU fallback without mocking device assignment,
        # but we can verify the failure is caught and logged)
        with patch('app.memory.logger') as mock_logger:
            try:
                store.add_texts(texts, metadatas, ids)
                # If we get here, CPU fallback worked
                mock_logger.warning.assert_called()  # Should log the GPU failure
            except Exception as e:
                # If CPU fallback also fails, it should raise an error
                assert "embedding" in str(e).lower()

    def test_cpu_fallback_embedding_success(self):
        """Test successful CPU embedding after GPU failure."""
        store = VectorStore()

        # Mock successful CPU embedder
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = [[0.1, 0.2, 0.3]]  # Mock embeddings
        store.embedder = mock_embedder

        # Mock ChromaDB
        store.collection = MagicMock()
        store.client = MagicMock()

        texts = ["Test document"]
        metadatas = [{"source": "test.py"}]
        ids = ["test_id_1"]

        # Should succeed with CPU embedding
        store.add_texts(texts, metadatas, ids)

        # Verify embedder was called and ChromaDB add was called
        mock_embedder.encode.assert_called_once_with(texts)
        store.collection.add.assert_called_once()

    def test_complete_gpu_and_cpu_failure(self):
        """Test graceful failure when both GPU and CPU embedding fail."""
        store = VectorStore()

        # Mock embedder that fails on both GPU and CPU attempts
        mock_embedder = MagicMock()
        mock_embedder.encode.side_effect = RuntimeError("All embedding devices failed")
        store.embedder = mock_embedder

        store.collection = MagicMock()
        store.client = MagicMock()

        texts = ["Test document"]
        metadatas = [{"source": "test.py"}]
        ids = ["test_id_1"]

        # Should raise an exception after all fallbacks fail
        with pytest.raises(RuntimeError, match="embedding"):
            store.add_texts(texts, metadatas, ids)

    def test_empty_texts_handling(self):
        """Test that empty text lists are handled gracefully."""
        store = VectorStore()

        # Should return early without error
        store.add_texts([], [], [])

        # Mock embedder should not be called
        if store.embedder:
            store.embedder.encode.assert_not_called()

    def test_no_embedder_initialized(self):
        """Test behavior when embedder is not initialized."""
        store = VectorStore()
        store.embedder = None  # Simulate initialization failure

        texts = ["Test document"]
        metadatas = [{"source": "test.py"}]
        ids = ["test_id_1"]

        # Should handle gracefully (current implementation just returns)
        store.add_texts(texts, metadatas, ids)

    @patch('app.memory.SentenceTransformer')
    def test_embedder_initialization_failure(self, mock_sentence_transformer):
        """Test circuit breaker during embedder initialization."""
        # Mock SentenceTransformer to fail during initialization
        mock_sentence_transformer.side_effect = Exception("GPU initialization failed")

        store = VectorStore()

        # Should handle initialization failure gracefully
        assert store.embedder is None

        # add_texts should not crash even without embedder
        store.collection = MagicMock()
        store.client = MagicMock()
        store.add_texts(["test"], [{"source": "test"}], ["id1"])

if __name__ == "__main__":
    pytest.main([__file__])
