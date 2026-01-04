import pytest
import os
import shutil
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.agents.librarian import LibrarianAgent

@pytest.fixture
def mock_container():
    container = MagicMock()
    # Mock L1 Driver
    container.l1_driver = MagicMock()
    container.l1_driver.generate = AsyncMock(return_value="This is a dense summary.")
    
    # Mock Storage
    container.storage = MagicMock()
    container.storage.upload = AsyncMock(return_value=True)
    
    # Mock Memory
    container.memory = MagicMock()
    container.memory.client = MagicMock()
    container.memory.client.upsert = MagicMock()
    container.memory.collection_name = "test_collection"
    container.memory.embedder = MagicMock()
    import numpy as np
    container.memory.embedder.encode = MagicMock(return_value=np.array([0.1] * 384))
    
    return container

@pytest.mark.asyncio
async def test_librarian_process_inbox(mock_container):
    # Setup
    inbox = "data/inbox"
    archive = "data/archive"
    os.makedirs(inbox, exist_ok=True)
    os.makedirs(archive, exist_ok=True)
    
    test_file = os.path.join(inbox, "test_doc.md")
    with open(test_file, "w") as f:
        f.write("This is some raw content for testing the librarian.")
    
    agent = LibrarianAgent(container=mock_container)
    
    # Run
    result = await agent.process_inbox()
    
    # Assert
    assert result["files_processed"] == 1
    assert result["status"] == "success"
    
    # Verify file moved
    assert not os.path.exists(test_file)
    assert os.path.exists(os.path.join(archive, "test_doc.md"))
    
    # Verify storage upload called with blob key
    mock_container.storage.upload.assert_called_once()
    args, kwargs = mock_container.storage.upload.call_args
    assert args[0].startswith("raw_")
    assert args[1] == "This is some raw content for testing the librarian."
    
    # Verify L1 summarize called
    mock_container.l1_driver.generate.assert_called_once()
    
    # Verify memory upsert called
    mock_container.memory.client.upsert.assert_called_once()
    
    # Cleanup
    if os.path.exists(os.path.join(archive, "test_doc.md")):
        os.remove(os.path.join(archive, "test_doc.md"))

@pytest.mark.asyncio
async def test_librarian_empty_inbox(mock_container):
    # Setup
    inbox = "data/inbox"
    if os.path.exists(inbox):
        for f in os.listdir(inbox):
            os.remove(os.path.join(inbox, f))
            
    agent = LibrarianAgent(container=mock_container)
    
    # Run
    result = await agent.process_inbox()
    
    # Assert
    assert result["files_processed"] == 0
    assert result["status"] == "success"
