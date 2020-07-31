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

        self.map = FastMap()
        self.map_compare = FastMap()
        self.stupid_tree = StupidTree()
        self.add_weight_1 = 10
        self.lose_weight_1 = 2
        self.lose_weight_2 = 50
        self.add_weight_2 = 99

    #入口，同时也是出口，向消息队列提供相似信息
    #返回值为InnerData，source 为InnerData.FastTree，value为SimpleNodeChain
    #add node weight not edge weight
    def add_simple_node_chain(self,chain:SimpleNodeChain):
        fast_chain = FastChain(chain,self.map,self.add_weight_1)
        self.pool.append(fast_chain)
        print(fast_chain.repeat_node_chain)
        if fast_chain.repeat_node_chain!=None:
            inner_data = InnerData(InnerData.FAST_TREE, fast_chain.repeat_node_chain)
            self.inner_message_queue.put(inner_data)

        self.lose_all_weight(self.lose_weight_1,self.map)


    def add_compare_data(self,inner_data:InnerData,messagelist):
        self.map_compare = FastMap()
        fast_chain = FastChain(inner_data.value, self.map_compare, self.add_weight_2)
        for i in range(20):
            if(i>len(messagelist)-1):
                break
            message = messagelist[(i+1)*-1]
            if (message.source == InnerData.OUTER_SEE):
                arr,has_flag = fast_chain.compare(message.value,self.map_compare)
                if(has_flag):
                    for item in arr:
                        self.stupid_tree.add_value(item[0])
        self.stupid_tree.say()


    def lose_all_weight(self,weight,map1:FastMap):
        for key in map1.get_map():
            map1.get_map().get(key).lose_all_weight(weight)








    def end_thread(self):
        self._thread_start = False

