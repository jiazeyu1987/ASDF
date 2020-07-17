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

        self.pool = []

        self.map = {}

    #入口，同时也是出口，向消息队列提供相似信息
    #返回值为InnerData，source 为InnerData.FastTree，value为SimpleNodeChain
    #add node weight not edge weight
    def add_simple_node_chain(self,chain:SimpleNodeChain):
        fast_chain = FastChain(chain,self.map)
        self.pool.append(fast_chain)
        self.analyse()

    def analyse(self):
        if(len(self.pool)<2):
            return



        if(len(self.pool)>g.fn_max_pool_deepth):
            chain0=self.pool.pop(0)
            #print(len(self.pool))
            chain0.release_fast_chain()
        last_chain = self.pool[-1]
        #last_chain.print()
        chain1 = last_chain.analyse_fast_chain()
        chain1.print()






    def end_thread(self):
        self._thread_start = False

