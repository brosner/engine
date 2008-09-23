
from engine.queues import QueueItem

queue = None

def defer(func, *args):
    """
    Queues the callable with the passed in arguments.
    """
    queue.put(QueueItem(func, args))
