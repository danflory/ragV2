"""
Test Memory Pruning Logic
Verifies deletion of old chunks before ingestion to prevent "Vector Rot".
"""
import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# Add the app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock external dependencies to avoid import errors
with patch.dict('sys.modules', {
    'asyncpg': MagicMock(),
    'chromadb': MagicMock(),
    'sentence_transformers': MagicMock(),
    'app.database': MagicMock(),
    'app.config': MagicMock(),
}):
    from app.memory import VectorStore


class TestMemoryPruning:
    """Test suite for memory pruning functionality."""

    @pytest.fixture
    def mock_vector_store(self):
        """Create a mock VectorStore with controllable behavior."""
        store = MagicMock(spec=VectorStore)
        store.collection = MagicMock()
        store.embedder = MagicMock()
        store.add_texts = MagicMock()
        store.prune_source_vectors = AsyncMock()
        return store

    @pytest.mark.asyncio
    async def test_prune_source_vectors_removes_old_chunks(self):
        """Test that prune_source_vectors deletes chunks with matching source_id."""
        # Create a real VectorStore instance with mocked collection
        store = VectorStore.__new__(VectorStore)
        store.collection = MagicMock()

        # Setup mock data
        source_id = "test_file.py"
        store.collection.get.return_value = {
            'ids': ['test_file_abc123', 'test_file_def456', 'other_file_xyz789'],
            'metadatas': [
                {'source': 'test_file.py'},
                {'source': 'test_file.py'},
                {'source': 'other_file.py'}
            ]
        }

        # Bind the real method to the instance
        store.prune_source_vectors = VectorStore.prune_source_vectors.__get__(store, VectorStore)

        # Execute
        result = await store.prune_source_vectors(source_id)

        # Verify
        assert result == 2
        store.collection.delete.assert_called_once_with(ids=['test_file_abc123', 'test_file_def456'])

    @pytest.mark.asyncio
    async def test_ingest_text_calls_pruning_before_ingestion(self):
        """Test that ingest_text prunes old vectors before adding new ones."""
        # Create real VectorStore instance for integration test
        store = VectorStore.__new__(VectorStore)  # Create without calling __init__

        # Mock the required attributes
        store.collection = MagicMock()
        store.embedder = MagicMock()
        store.add_texts = MagicMock()

        # Mock prune_source_vectors
        store.prune_source_vectors = AsyncMock(return_value=3)

        # Add the real ingest_text method
        store.ingest_text = VectorStore.ingest_text.__get__(store, VectorStore)

        # Test data
        test_content = "def hello():\n    return 'world'"
        test_metadata = {"source": "app/main.py", "type": "code_repository"}

        # Execute
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value.hex = 'test123'
            await store.ingest_text(test_content, test_metadata)

        # Verify pruning was called
        store.prune_source_vectors.assert_called_once_with("app/main.py")

        # Verify new content was added after pruning
        store.add_texts.assert_called_once()
        args = store.add_texts.call_args[0]
        assert args[0] == [test_content]  # texts
        assert args[1] == [test_metadata]  # metadatas
        assert len(args[2]) == 1  # ids (should have one ID)

    @pytest.mark.asyncio
    async def test_prune_handles_empty_collection(self):
        """Test pruning behavior when no chunks exist for the source."""
        store = VectorStore.__new__(VectorStore)
        store.collection = MagicMock()
        store.collection.get.return_value = {'ids': [], 'metadatas': []}
        store.prune_source_vectors = VectorStore.prune_source_vectors.__get__(store, VectorStore)

        source_id = "nonexistent.py"
        result = await store.prune_source_vectors(source_id)

        assert result == 0
        store.collection.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_prune_handles_collection_error(self):
        """Test graceful handling of collection access errors during pruning."""
        store = VectorStore.__new__(VectorStore)
        store.collection = MagicMock()
        store.collection.get.side_effect = Exception("Collection unavailable")
        store.prune_source_vectors = VectorStore.prune_source_vectors.__get__(store, VectorStore)

        source_id = "error_source.py"

        # Should not raise exception
        result = await store.prune_source_vectors(source_id)

        assert result == 0  # Returns 0 on error

    @pytest.mark.asyncio
    async def test_ingestion_workflow_with_pruning(self):
        """Integration test: Full workflow from prune -> ingest."""
        store = VectorStore.__new__(VectorStore)
        store.collection = MagicMock()
        store.embedder = MagicMock()
        store.add_texts = MagicMock()

        # Track call order
        call_order = []

        async def mock_prune(source_id):
            call_order.append(f"prune_{source_id}")
            return 2

        store.prune_source_vectors = mock_prune
        store.ingest_text = VectorStore.ingest_text.__get__(store, VectorStore)

        # Execute workflow
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value.hex = 'abc123'
            await store.ingest_text("new content", {"source": "updated_file.py"})

        # Verify call order: prune first, then add
        assert call_order == ["prune_updated_file.py"]
        assert store.add_texts.called

        # Verify the ID generation includes source
        args = store.add_texts.call_args[0]
        generated_id = args[2][0]  # First ID in the list
        assert "updated_file.py_abc123" == generated_id
