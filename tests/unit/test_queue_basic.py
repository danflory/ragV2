import asyncio
import pytest
from app.services.scheduler.queue import RequestQueue

@pytest.mark.asyncio
async def test_basic_enqueue_dequeue():
    queue = RequestQueue()
    request_data = {"task": "test_task"}
    
    await queue.enqueue(request_data, priority=10)
    assert queue.qsize() == 1
    
    result = await queue.dequeue()
    assert result == request_data
    assert queue.empty() is True

@pytest.mark.asyncio
async def test_multiple_items_fifo_same_priority():
    queue = RequestQueue()
    await queue.enqueue("task1", priority=10)
    await queue.enqueue("task2", priority=10)
    
    assert await queue.dequeue() == "task1"
    assert await queue.dequeue() == "task2"
