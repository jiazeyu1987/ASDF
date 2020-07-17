from .. import NodeBase
import  globalconfig as g
class FastNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge_map = {}


    def add_node(self,node1):
        from . import FastEdge
        if(node1.value in self.follow_edge_map):
            self.follow_edge_map[node1.value].add_weight()
        else:
            edge = FastEdge(self, node1)
            edge.add_weight()
            self.follow_edge_map[node1.value] = edge
        return self.follow_edge_map[node1.value]

    def is_strong_enough(self):
        return self.strong>1+g.add_weight_number


    def lose_weight(self):
        if(self.strong>1):
            self.strong-=1