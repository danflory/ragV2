import asyncio
import itertools
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class QueuedItem:
    priority: int
    sequence: int  # To ensure FIFO for equal priorities
    request: Any = field(compare=False)

class RequestQueue:
    """
    A priority-aware asynchronous request queue.
    Lower priority values are dequeued first.
    0 = Standard High Priority
    10 = Default
    -1 = Mr. Big Guy (Jumps the line)
    """
    def __init__(self):
        self._queue = asyncio.PriorityQueue()
        self._counter = itertools.count()

    async def enqueue(self, request: Any, priority: int = 10):
        """
        Add a request to the queue.
        """
        count = next(self._counter)
        await self._queue.put(QueuedItem(priority=priority, sequence=count, request=request))

    async def push_to_front(self, request: Any):
        """
        Force a request to the front of the queue by using the highest possible priority.
        """
        # We use -1 to jump ahead of priority 0. 
        # For sequence, it will still follow other -1s in order, 
        # but will jump everything else.
        await self.enqueue(request, priority=-1)

    async def dequeue(self) -> Any:
        """
        Retrieve the next request from the queue.
        """
        item = await self._queue.get()
        return item.request

    def qsize(self) -> int:
        return self._queue.qsize()

    def empty(self) -> bool:
        return self._queue.empty()
