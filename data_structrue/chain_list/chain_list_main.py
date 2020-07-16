import data_structrue as ds
from .. import *
import globalconfig as g
# 省略了信息源问题
from threading import Thread, Event
class ChainListMain(Thread):
    def __init__(self, inner_message_queue,fast_tree):
        Thread.__init__(self)
        self.inner_message_queue = inner_message_queue
        self.block_timeout = 1
        self.fast_tree= fast_tree
        self.chain_list = []


    def run(self):
        while True:
            try:
                inner_data  = self.inner_message_queue.get(True,self.block_timeout)
                if(inner_data.value==g.sleep_symbol):
                    self.fast_tree.end_thread()
                    return
                else:
                    self.addItem(inner_data)
            except Exception:
                pass

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
        if(inner_data.source == InnerData.OUTER):
            self.fast_tree.add_value(inner_data.value)
        pass



    def print(self):
        for chain in self.chain_list:
            chain.print()
