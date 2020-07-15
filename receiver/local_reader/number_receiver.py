from threading import Thread, Event
from queue import Queue
import time
import random
import globalconfig as g
from data_structrue import *
from . import *
class NumberReceiver(Thread):
    def __init__(self, queue):
        self.active_node = None
        Thread.__init__(self)
        #多线程共享容器
        self.queue = queue
        #触发无聊代码的时间
        self.block_timeout = 1
        #有效字符数组
        self.char_array = []
        #无聊代码的个数
        self.gap_number = 0
        self.chainlist = ChainListMain()
    '''
        eye 会将看到的内容逐个放入queue中
        run 方法从queue中提取数据
        如果queue没有数据，会每隔block_timeout添加一个无聊代码->g.time_gap_symbol
    '''
    def run(self):
        while True:
            try:
                item  = self.queue.get(True,self.block_timeout)
                self.addItem(item)

            except Exception:
                self.addItem(g.time_gap_symbol)
                self.chainlist.print()
                return


    '''
        判断接收到的内容是eye看到的字符，还是无聊代码
    '''
    def addItem(self,char_val):
        if(char_val!=g.time_gap_symbol):
            self.awake(char_val)
        else:
            self.asleep()


    '''
        如果接受到的是有效字符
        1.接收到的是分隔符
            1.如果接收到的是1个分隔符
            2.如果接受到的是多个分隔符
        2.接收到的是非分隔符
            1.起始字符，前面有大段的无聊期，无上下关联，开始一段数据
            2.起始字符，刚刚遇到了分隔符，前面有关联
            3.非起始字符
    '''
    def awake(self,char_val):
        self.gap_number = 0
        if(char_val in g.time_gap):
            if(g.time_gap[char_val]>1):
                self.submit()
                self.char_array = []
                return
        self.char_array.append(char_val)
        if(len(self.char_array)>g.max_char_can_handle):
            self.submit()
            self.char_array = []
            return



    def asleep(self):
        self.gap_number+=1
        if(self.gap_number>g.max_time_gap_symbol_to_handle):
            if(len(self.char_array)!=0):
                self.submit()
                self.char_array = []
                return


    def submit(self):
        #print(self.char_array)
        self.char_str = change_array_to_str(self.char_array)

        #处理数据的数据结构
        simple_node_chain = SimpleNodeChain()
        simple_node_chain.on_data_enter(change_raw_string_to_gap_string(self.char_str))
        self.chainlist.add_chain(simple_node_chain)
        pass

