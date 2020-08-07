from .. import NodeBase,EdgeBase
import  globalconfig as g
class StupidNode(NodeBase):
    def __init__(self,value,flag):
        super().__init__(value,flag)
        self.unique = False
        self.type = "stupid"
        self.follow_edge_map = {}

    @staticmethod
    def create_node(value):
        if (value in NodeBase.all_map):
            pass
        else:
            NodeBase.all_map[value] = StupidNode(value, "lfljaskdfj")
        node1 = NodeBase.all_map[value]
        nc = node1.copy()
        node1.link(nc, NodeBase.TYPE_CHILD)
        return nc

    def copy(self):
        node = StupidNode(self.get_value(),"lfljaskdfj")
        node.strong = self.strong
        node.type = self.type
        return node

