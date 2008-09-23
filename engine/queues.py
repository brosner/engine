
import socket

try:
    import cPickle as pickle
except ImportError:
    import pickle

class QueueItem(object):
    """
    Encapsulates a single queue item that is put on the queue for a listener
    to grab and do something with.
    """
    def __init__(self, func, args):
        self.func = func
        self.args = args
    
    def execute(self):
        """
        Execute this queue item based on the stored values.
        """
        self.func(*args)

class BaseQueue(object):
    """
    Basic interface of a queue.
    """
    def add(self, item):
        raise NotImplemented()

class DummyQueue(BaseQueue):
    """
    A queue that will execute on put. This is useful for using the engine
    queue API without having a backing message queue handling system.
    """
    def put(self, item):
        """
        Execute the given item right away.
        """
        item.execute()

class StompQueue(BaseQueue):
    """
    A STOMP compliant queue.
    """
    def __init__(self):
        import stomp
        try:
            self._conn = stomp.Connection()
            self._conn.start()
            self._conn.connect()
        except socket.error:
            pass # TODO: understand why the library recommends this.
    
    def put(self, item):
        """
        Pickle the queue item and hand it off to the STOMP queue named
        /queue/[function_name].
        """
        message = pickle.dumps(item)
        self._conn.send(message, destination="/queue/%s" % item.func.__name__)
