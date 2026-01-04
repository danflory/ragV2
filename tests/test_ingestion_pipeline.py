import pytest
import os
import shutil
import tempfile
from unittest.mock import AsyncMock, MagicMock
from app.ingestor import DocumentIngestor

@pytest.mark.asyncio
async def test_ingest_all_workflow():
    """
    Tests the ingestion pipeline:
    1. Scan directory
    2. Filter extensions (.md, .txt, .py)
    3. Chunk content
    4. Call vector_store.ingest
    """
    # 1. Setup temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Create some dummy files
        files_to_create = {
            "doc1.md": "This is a markdown file content.",
            "code.py": "print('hello')",
            "notes.txt": "Some text notes.",
            "ignore.json": '{"key": "value"}'
        }
        
        for name, content in files_to_create.items():
            with open(os.path.join(temp_dir, name), "w") as f:
                f.write(content)

        # 2. Mock dependencies
        mock_vector_store = MagicMock()
        mock_vector_store.ingest = AsyncMock(return_value=True)
        mock_storage = MagicMock()

        # 3. Initialize Ingestor
        ingestor = DocumentIngestor(vector_store=mock_vector_store, storage=mock_storage)
        ingestor.docs_path = temp_dir  # Override path for test

        # 4. Run ingestion
        await ingestor.ingest_all()

        # 5. Assertions
        # Should have called ingest for .md, .py, .txt
        # Total files: 3 (doc1.md, code.py, notes.txt)
        assert mock_vector_store.ingest.call_count == 3
        
        # Verify metadata
        calls = mock_vector_store.ingest.call_args_list
        sources = [c.args[1]["source"] for c in calls]
        
        assert "doc1.md" in sources
        assert "code.py" in sources
        assert "notes.txt" in sources
        assert "ignore.json" not in sources

    finally:
        shutil.rmtree(temp_dir)

@pytest.mark.asyncio
async def test_chunking_logic():
    """
    Verifies that files larger than 1000 characters are chunked correctly.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        # 2500 characters
        large_content = "A" * 2500
        file_path = os.path.join(temp_dir, "large.md")
        with open(file_path, "w") as f:
            f.write(large_content)

        mock_vector_store = MagicMock()
        mock_vector_store.ingest = AsyncMock(return_value=True)
        mock_storage = MagicMock()

        ingestor = DocumentIngestor(vector_store=mock_vector_store, storage=mock_storage)
        ingestor.docs_path = temp_dir

        await ingestor.ingest_all()

        # 2500 chars / 1000 per chunk = 3 chunks
        assert mock_vector_store.ingest.call_count == 3
        
        # Verify chunk indices in metadata
        calls = mock_vector_store.ingest.call_args_list
        indices = [c.args[1]["chunk_index"] for c in calls]
        assert indices == [0, 1, 2]

    finally:
        shutil.rmtree(temp_dir)
