import asyncio
import pytest
from app.services.scheduler.queue import RequestQueue

@pytest.mark.asyncio
async def test_priority_jumping():
    queue = RequestQueue()
    
    # Enqueue low priority items
    await queue.enqueue("low1", priority=20)
    await queue.enqueue("low2", priority=20)
    
    # Enqueue a high priority item
    await queue.enqueue("high1", priority=0)
    
    # Enqueue "Mr. Big Guy"
    await queue.push_to_front("big_guy")
    
    # Should dequeue in order: big_guy, high1, low1, low2
    assert await queue.dequeue() == "big_guy"
    assert await queue.dequeue() == "high1"
    assert await queue.dequeue() == "low1"
    assert await queue.dequeue() == "low2"

@pytest.mark.asyncio
async def test_fifo_preservation():
    queue = RequestQueue()
    
    # Enqueue items with same priority
    await queue.enqueue("first", priority=10)
    await queue.enqueue("second", priority=10)
    await queue.enqueue("third", priority=10)
    
    assert await queue.dequeue() == "first"
    assert await queue.dequeue() == "second"
    assert await queue.dequeue() == "third"
