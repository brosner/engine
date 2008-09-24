#!/usr/bin/env python

import time
import stomp
import logging

try:
    import cPickle as pickle
except ImportError:
    import pickle

class QueueListener(object):
    def on_error(self, headers, message):
        logging.info(message)
    
    def on_message(self, headers, message):
        queue_item = pickle.loads(message)
        queue_item.execute()

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    conn = stomp.Connection()
    conn.add_listener(QueueListener())
    conn.start()
    time.sleep(2)
    conn.connect()
    conn.subscribe(destination="/queue/hello_world", ack="auto")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
