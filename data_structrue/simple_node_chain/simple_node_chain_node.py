from .. import NodeBase
class SimpleNodeChainNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)


    def get_next_node(self):
        from .. import EdgeBase
        for edge in self.edge_list:
            if(edge.type!=EdgeBase.TYPE_NORMAL):
                continue
            return edge.node_to

    def remove_edge(self):
        self.follow_edge = None




    def replace_next_node(self,node1):
        from . import SimpleNodeChainEdge
        from .. import EdgeBase
        for edge in self.edge_list:
            edge.node_to = node1








    def add_edge(self,edge):
        self.follow_edge = edge


