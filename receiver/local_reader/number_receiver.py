from threading import Thread, Event
from queue import Queue
import time
import random
import globalconfig as g
from data_structrue import *
class NumberReceiver(Thread):
    def __init__(self, queue):
        self.active_node = None
        Thread.__init__(self)
        self.queue = queue
        self.tree1 = Tree1()

    def run(self):
        while True:
            try:
                item  = self.queue.get(True,1)
                self.addItem(item)
            except Exception:
                self.addItem(g.time_gap_symbol)


    def addItem(self,char_val):
        if(char_val!=g.time_gap_symbol):
            self.awake(char_val)
        else:
            self.asleep()


    def awake(self,char_val):
        if(self.active_node==None):
            self.active_node = self.tree1.new(char_val)
        self.tree1.append(self.active_node,char_val)



    def asleep(self):
        pass

