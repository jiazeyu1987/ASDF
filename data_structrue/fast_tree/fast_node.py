from .. import NodeBase
class FastNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge_list = []


    def add_edge(self,edge):
        self.follow_edge_list.append(edge)
