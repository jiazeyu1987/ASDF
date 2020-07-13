from . import *
class Node1:
    def __init__(self,value):
        self.value = value
        self.edgelist = []
        pass


    def append_value(self,value):
        node_new = Node1(value)
        edge = Edge1(self,node_new)
        self.edgelist.append(edge)


