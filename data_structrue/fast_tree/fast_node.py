from .. import NodeBase
import  globalconfig as g
class FastNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge_map = {}
        self.strong = 0


    def add_node(self,node1,edge_weight):
        from . import FastEdge
        flag = False
        if(node1.value in self.follow_edge_map):
            self.follow_edge_map[node1.value].add_weight(edge_weight)
            if(node1.strong>0 and self.follow_edge_map[node1.value].strong>0):
                flag = True
        else:
            edge = FastEdge(self, node1)
            edge.add_weight(edge_weight)
            self.follow_edge_map[node1.value] = edge
        return self.follow_edge_map[node1.value],flag

    def lose_all_weight(self,weight):
        self.strong-=weight
        for edge in self.follow_edge_map:
            self.follow_edge_map[edge].lose_weight(weight)
