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
            # if(i==50):
            #     time.sleep(100)
            self.queue.put(value[i])



