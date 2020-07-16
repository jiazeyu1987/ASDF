from .. import *
from ..simple_node_chain import SimpleNodeChain
from threading import Thread, Event
from . import *
class FastTree(Thread):
    def __init__(self, queue):
        Thread.__init__(self)

        self.root = FastNode("")
        # 多线程共享容器
        self.queue = queue

        self._thread_start = True

        self.map = {}

    #入口，同时也是出口，向消息队列提供相似信息
    #add node weight not edge weight
    def add_value(self,str_value:str):
        #print("F",value)
        head_node = None
        for char1 in str_value:
            if(char1 in self.map):
                self.map[char1].strong+=1
            else:
                self.map[char1] = FastNode(char1)
            if(head_node==None):
                head_node = self.map[char1]
            else:
                self.link_to(head_node,self.map[char1])
                head_node = self.map[char1]

    def link_to(self,node_from,node_to):
        pass

    def end_thread(self):
        self._thread_start = False

