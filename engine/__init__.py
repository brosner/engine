
from engine.queues import DummyQueue, QueueItem

default_queue = DummyQueue()

def defer(func, *args, queue=None):
    """
    Queues the callable with the passed in arguments.
    """
    if queue is None:
        queue = default_queue
    queue.put(QueueItem(func, args))
