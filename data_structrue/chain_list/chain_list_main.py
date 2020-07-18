import data_structrue as ds
from .. import InnerData
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
        if(inner_data.source == InnerData.OUTER_SEE):
            self.fast_tree.add_simple_node_chain(inner_data.value)
            self.chain_list.append(inner_data.value)
        elif(inner_data.source == InnerData.FAST_TREE):
            #print(inner_data.value)
            if(g.g_ps_desire_point<5):
                pass

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
        每条消息流的处理有三种可能
        1.有一个或者若干个成熟的处理模块来处理它
        2.存在一个或者若干个处理模块，但是不确定其正确性
        3.不存在处理模块来处理
        
        *消息处理模块*
        消息处理模块是若干个内置消息处理单元的组合
        
        *消息处理单元*
        
        
        
    '''





    def print(self):
        for chain in self.chain_list:
            chain.print()
