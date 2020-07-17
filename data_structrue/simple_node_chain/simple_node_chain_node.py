from .. import NodeBase
class SimpleNodeChainNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge = None

    def get_next_node(self):
        if(self.follow_edge==None):
            return None
        if(self.follow_edge.node_to==None):
            return None
        return self.follow_edge.node_to

    def add_edge(self,edge):
        self.follow_edge = edge


