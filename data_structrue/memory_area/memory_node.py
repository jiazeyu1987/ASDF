import globalconfig as g
from .. import NodeBase
from . import *
class MemoryNode(NodeBase):
    MEMORY_NODE_ID = 1
    def __init__(self,value1=g.g_mm_empty_symbol):
        super().__init__(value1)
        self.id = MemoryNode.MEMORY_NODE_ID
        MemoryNode.MEMORY_NODE_ID+=1
        self.follow_edge_map = {}

    def add_node(self,node1,edge_type=MemoryEdge.EDGE_NORMAL):
        if(node1.value in self.follow_edge_map):
            self.follow_edge_map[node1.value].add_weight()
        else:
            edge = MemoryEdge(self, node1,edge_type)
            edge.add_weight()
            self.follow_edge_map[node1.value] = edge
        return self.follow_edge_map[node1.value]

    def get_str1(self,n,map1):
        head = n*"  "
        str1 = head
        str1 = str1 + self.id.__str__() + ":" + self.value + "\n"
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            if(edge.id in map1):
                continue
            map1[edge.id]=1
            node_to = edge.node_to
            str1 = str1 + head +edge.get_type()+ node_to.get_str1(n+1,map1) + "\n"
        return str1

    def say(self):
        print(self.get_str1(0,{}))

