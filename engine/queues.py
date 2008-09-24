
import time
import socket

try:
    import cPickle as pickle
except ImportError:
    import pickle

__all__ = ("QueueItem", "DummyQueue", "StompQueue",)

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
        self.func(*self.args)

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

class StompProtocol(object):
    def __init__(self, host="127.0.0.1", port=61613):
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self._sock.connect((self.host, self.port))
    
    def connect_to_queue(self):
        # TODO: support authenicated access
        self._send_frame("CONNECT")
    
    def disconnect(self):
        self._send_frame("DISCONNECT")
    
    def send(self, destination, message):
        headers = {"destination": destination}
        self._send_frame("SEND", payload=message, headers=headers)
    
    def _send_frame(self, command, headers=None, payload=None):
        if self._sock is not None:
            if headers is not None:
                _headers = []
                for key, value in headers.items():
                    _headers.append("%s:%s\n" % (key, value))
                headers = "".join(_headers)
            else:
                headers = ""
            if payload is None:
                payload = ""
            frame = "%s\n%s\n%s\x00" % (command, headers, payload)
            self._sock.sendall(frame)
        else:
            # XXX: have an Exception subclass
            raise Exception, "not connected"

class StompQueue(BaseQueue):
    """
    A STOMP compliant queue.
    """
    protocol_class = StompProtocol
    
    def __init__(self, **kwargs):
        self.protocol = self.protocol_class(**kwargs)
        self.protocol.connect()
        self.protocol.connect_to_queue()
    
    def put(self, item):
        """
        Pickle the queue item and hand it off to the STOMP queue named
        /queue/[function_name].
        """
        message = pickle.dumps(item)
        self.protocol.send("/queue/%s" % item.func.__name__, message)
