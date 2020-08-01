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

    def remove_edge(self):
        self.follow_edge = None

    def replace_next_node(self,node1):
        from . import SimpleNodeChainEdge
        from .. import EdgeBase
        old_edge = self.follow_edge
        if(old_edge!=None):
            old_node_to = old_edge.node_to
            edge = SimpleNodeChainEdge(node1, old_node_to)
            node1.replace_edge = edge
        edge = SimpleNodeChainEdge(self,node1)
        edge.type = EdgeBase.TYPE_NORMAL
        self.follow_edge = edge








    def add_edge(self,edge):
        self.follow_edge = edge


