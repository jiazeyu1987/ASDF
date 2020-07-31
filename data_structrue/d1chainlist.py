import data_structrue as ds
from data_structrue import InnerData
import globalconfig as g
from threading import Thread, Event
from queue import Queue
from . import *
class D1ChainList(Thread):
    def __init__(self, inner_message_queue:Queue,fast_tree,exception_queue:Queue):
        Thread.__init__(self)
        self.inner_message_queue = inner_message_queue
        self.block_timeout = 1
        self.fast_tree= fast_tree
        self.exception_queue = exception_queue
        self.chain_list = []
        self._search_index = -1
        self.message_cache = []


    def run(self):
        import sys,queue
        try:
            while True:
                inner_data  = self.inner_message_queue.get(True)
                self.message_cache.append(inner_data)
                if(len(self.message_cache)>g.g_d1c_max_search_depth):
                    self.message_cache.pop(0)

                if(inner_data.value==g.sleep_symbol):
                    self.fast_tree.end_thread()
                    return
                else:
                    self.addItem(inner_data)
        except queue.Empty:
            g.main = False
        except Exception:
            self.exception_queue.put(sys.exc_info())

    # 获取了一条新的信息
    # 获取到的新的信息可能有以下几个可能
    # 1.陈述句，描述结构
    # 2.疑问句，询问结构
    # 3.未识别单元
    # 4.未识别句型
    '''
        1.陈述句，描述结构
        描述结构分为以下几种可能
            1.普通陈述句
                1.之前已描述过此类结构
                    又有以下几种可能
                        1.之前描述过的结构与此次完全相同
                        2.之前描述过的结构与此次部分相同，又分为此次是之前的子集，此次是之前的超集
                2.之前未描述过此类结构
            2.对比陈述句
                对比陈述句要求词组长度相同，内容只有一项不同，将不同项合并为一个或者融合入一个类别
                对比陈述句的不同处可能在开头，可能在中间，可能在结尾
    '''
    def addItem(self,inner_data:InnerData):
        g.p("d1c", inner_data.__str__())
        if(inner_data.source == InnerData.OUTER_SEE):
            self.fast_tree.add_simple_node_chain(inner_data.value)
            self.chain_list.append(inner_data.value)
        elif(inner_data.source == InnerData.FAST_TREE):
            if(g.g_ps_desire_point<5):
                self.fast_tree.add_compare_data(inner_data, self.message_cache)
        elif(inner_data.source==g.entity_book_name):
            eh.do_exec(inner_data)




    def clear_search_index(self):
        self._search_index = -1

    def location_inner_data(self,idata):
        if (self._search_index * -1 == len(self.message_cache) + 1):
            return False
        for i in range(g.g_d1c_max_search_depth):
            v = (self.message_cache[self._search_index].source)
            if(self.message_cache[self._search_index]==idata):
                self._search_index-=1
                return True
            else:
                self._search_index-=1
                if (self._search_index * -1 == len(self.message_cache) + 1):
                    return False
        return False

    def location_inner_type(self,data_type):
        if (self._search_index * -1 == len(self.message_cache) + 1):
            return False
        for i in range(g.g_d1c_max_search_depth):
            if(self.message_cache[self._search_index].source==data_type):
                self._search_index-=1
                return True
            else:
                self._search_index-=1
                if (self._search_index * -1 == len(self.message_cache) + 1):
                    return False
        return False

    '''
        *消息流的特点*
        1.当有很重要的消息进入的时候立刻终止对其他消息的处理，可以记录断点
        2.消息有重要程度的区别，优先处理重要的消息
        3.消息处理分为主处理器处理和副处理器处理，副处理器是无意识的，自动处理响应的消息，主处理器是有意识的，选择处理消息
          PS：FastTree是副处理器中的一个
        4.从外部接收到的信息会先做预处理，来判定消息级别
        5.如果主处理器正在专心处理一条消息而放弃对其他消息做预处理，那么称之为处于沉浸状态
        6.处于警戒状态的主处理器不会处于沉浸状态
        
        当接收到FastTree的有效消息之后
        1.前方无高等优先命令，选择处理它
            FastTree的消息处理属于【消息流处理】中的第一条：有一个或者若干个成熟的处理模块来处理它
            FastTree的消息处理属于内置的
        2.前方有高等优先命令，忽略它
        
        *消息流的处理*
        消息流在主处理器中处理
        每条消息流的处理有三种可能
        1.有一个或者若干个成熟的处理模块来处理它
        2.存在一个或者若干个处理模块，但是不确定其正确性
        3.不存在处理模块来处理
        
        *消息处理模块*
        消息处理模块是若干个内置消息处理单元的组合
        
        *消息处理单元*
        1
        
        *二维印象区*
        二维印象区是一个Width*Height大小的二维数组
        二维印象区有缓存功能，能够缓存若干页面，超过缓存区大小的被遗忘
        二维印象区的内容可以被永久映射到主存储区，主存储区的内容也可以映射到二维印象区
        一维印象区是二维印象区的特例
        二维印象区的页面代表着时间先后关系
        
        
    '''





    def print(self):
        for chain in self.chain_list:
            chain.print()
