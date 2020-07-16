from threading import Thread, Event
from queue import Queue
import time
import random
from . import *
class Eye(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        value = read_file(g.entity_book_name)
        for i in range(len(value)):
            self.queue.put(value[i])
            time.sleep(0.1)
        time.sleep(1)
        self.queue.put("\n")
        self.queue.put(g.sleep_symbol)


