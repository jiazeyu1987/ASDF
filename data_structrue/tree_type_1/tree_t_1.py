from . import *
import globalconfig as g
class Tree1:
    def __init__(self):
        self.head = None

    #从receiver/eye异步接收到的数据
    def on_data_enter(self,char_str):
        start_index = -1
        for i in range(len(char_str)):
            char1 = char_str[i]
            if (char1 == g.time_gap_symbol):
                if(start_index!=-1):
                    val = char_str[start_index:i]
                    start_index = -1
                    self.enter_node_val(val)
            else:
                if(start_index==-1):
                    start_index = i
        print_head(self.head)
        self.head = None

    def print_head(self,head):
        pass

    def enter_node_val(self,val):
        if(self.head==None):
            self.head = self.new(val)
        else:
            pass

    def new(self,val):
        return Node1(val)

