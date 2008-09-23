
from engine.queues import DummyQueue, QueueItem

default_queue = DummyQueue()

def defer(func, *args, **kwargs):
    """
    Queues the callable with the passed in arguments.
    """
    queue = kwargs.pop("queue", default_queue)
    queue.put(QueueItem(func, args))
