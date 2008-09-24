
from engine.queues import *

default_queue = DummyQueue()

def configure(**options):
    """
    Configure the engine.
    """
    global default_queue
    default_queue = options.get("queue", default_queue)

def defer(func, *args, **kwargs):
    """
    Queues the callable with the passed in arguments.
    """
    queue = kwargs.pop("queue", default_queue)
    queue.put(QueueItem(func, args))
