from . import *
from .. import *
import globalconfig as g
class StupidTree:
    def __init__(self):
        self.root = StupidNode("擱")

    def add_value(self,arrlist,final_node,final_edge_type):
        current_node = self.root
        for char in arrlist:
            new_node = current_node.add_node(char)
            current_node = new_node
        current_node.link(final_node,final_edge_type)
        # uni.unique = True
    def add_chain(self,chain:SimpleNodeChain):
        head = chain.get_head()
        current_node = self.root
        while True:
            head = head.get_next_node()
            if(head==None):
                break
            new_node = current_node.add_node(head.get_value())
            current_node = new_node



    def get_nearest(self,value1):
        return self.root.get_nearest(value1)




    def say(self):
        self.root.say()