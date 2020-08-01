from data_structrue import NodeBase,EdgeBase
from . import *
class SpecialNode(NodeBase):
    def __init__(self):
        super().__init__("")
        self.type = NodeBase.TYPE_SPECIAL

    def add_special_child(self,value,c):
        node = None
        if(value in self.follow_edge_map):
            node = self.follow_edge_map[value].node_to
        else:
            node = SpecialChildNode()
            node.value = value
            self.link_map(node,EdgeBase.TYPE_NORMAL,value)
        value_node = ValueNode(c)
        node.link_map(value_node,EdgeBase.TYPE_NORMAL,value_node.id.__str__())


    def compare(self,node1):
        from . import EntityNode
        arr = []
        for key in self.follow_edge_map:
            if(key in node1.follow_edge_map):
                pass
            else:
                arr.append(CompareValue(EntityNode.COMPARE_LACK,self.follow_edge_map[key].node_to,None))

        for key in node1.follow_edge_map:
            if(key in self.follow_edge_map):
                pass
            else:
                arr.append(CompareValue(EntityNode.COMPARE_MORE,None,node1.follow_edge_map[key].node_to))

        for key in self.follow_edge_map:
            if(key in node1.follow_edge_map):
                arr = arr+self.follow_edge_map[key].node_to.compare(node1.follow_edge_map[key].node_to)
        return arr
