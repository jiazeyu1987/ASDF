from .. import *
from ..simple_node_chain import SimpleNodeChain
from threading import Thread, Event
from . import *
from queue import Queue
class FastTree(Thread):
    def __init__(self, inner_message_queue:Queue):
        Thread.__init__(self)

        self.root = FastNode("")
        # 多线程共享容器
        self.inner_message_queue = inner_message_queue

        self._thread_start = True

        self.pool = []

        self.map = {}

    #入口，同时也是出口，向消息队列提供相似信息
    #返回值为InnerData，source 为InnerData.FastTree，value为SimpleNodeChain
    #add node weight not edge weight
    def add_simple_node_chain(self,chain:SimpleNodeChain):
        fast_chain = FastChain(chain,self.map)
        self.pool.append(fast_chain)
        chain1 = self.get_result_of_compare_fast_chain()
        if (chain1 == None):
            return
        if (chain1.head == g.replace_symbol and chain1.head.get_next_node == None):
            return
        else:
            inner_data = InnerData(InnerData.FAST_TREE,chain1)
            g.p("ft","enter:"+chain.__str__())
            g.p("ft","got:"+chain1.__str__())
            self.inner_message_queue.put(inner_data)

    def get_result_of_compare_fast_chain(self):
        if(len(self.pool)<2):
            return
        if(len(self.pool)>g.g_fn_max_pool_deepth):
            chain0=self.pool.pop(0)
            chain0.release_fast_chain()
        last_chain = self.pool[-1]
        chain1 = last_chain.get_fast_compare_result()
        return chain1







    def end_thread(self):
        self._thread_start = False

