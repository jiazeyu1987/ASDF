from . import *
import globalconfig as g
class SimpleNodeChain:
    def __init__(self):
        self.head = None
        #current node
        self.current_node = None

    def get_head(self)->SimpleNodeChainNode:
        return self.head

    #从receiver/eye异步接收到的数据
    def on_data_enter(self,char_str):
        # start_index = -1
        # len1 = len(char_str)
        # for i in range(len1):
        #     char1 = char_str[i]
        #     if (char1 == g.time_gap_symbol):
        #         if(start_index!=-1):
        #             val = char_str[start_index:i]
        #             start_index = -1
        #             self.enter_node_val(val)
        #     else:
        #         if(start_index==-1):
        #             start_index = i
        #         if(i==len1-1):
        #             val = char_str[start_index:len1]
        #             start_index = -1
        #             self.enter_node_val(val)
        for char1 in char_str:
            self.enter_node_val(char1)


    def __str__(self):
        str1 = "simple node chain info:"
        tmp_node = self.head
        index = 1
        while True:
            if (tmp_node == None):
                break
            if (index > 50):
                break
            index += 1
            str1 = str1 + tmp_node.value + " - "
            if (tmp_node.follow_edge == None):
                break
            tmp_node = tmp_node.follow_edge.node_to
        return str1

    def enter_node_val(self,val):
        if(self.head==None):
            self.head = self.new(val)
            self.current_node = self.head
        else:
            new_node = self.new(val)
            self.link(self.current_node,new_node)
            self.current_node = new_node




    def link(self,node_from:SimpleNodeChainNode,node_to:SimpleNodeChainNode):
        from .simple_node_chain_edge import SimpleNodeChainEdge
        SimpleNodeChainEdge = SimpleNodeChainEdge(node_from,node_to)
        node_from.follow_edge= SimpleNodeChainEdge



    def new(self,val):
        return SimpleNodeChainNode(val)

