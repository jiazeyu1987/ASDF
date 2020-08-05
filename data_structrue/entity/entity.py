from . import *
from data_structrue import NodeBase,EdgeBase
class EntityNode(NodeBase):
    NODE_TIME = "time"
    NODE_ADDRESS = "address"
    NODE_SPECIAL = "special"
    NODE_NUMBER = "number"
    NODE_ACTION = "action"


    def __init__(self,value):
        super().__init__(value)
        self.type = NodeBase.TYPE_ENTITY
        # self.add_time_node()
        # self.add_address_node()
        # self.add_number_node()
        # self.add_special_node()

    def copy(self):
        node = EntityNode(self.get_value())
        node.value = self.get_value()
        node.strong = self.strong
        node.type = self.type
        return node

    # def add_time_node(self):
    #     time_node = TimeNode()
    #     self.link_map(time_node,EdgeBase.TYPE_NORMAL,EntityNode.NODE_TIME)
    #
    #
    # def add_address_node(self):
    #     address_node = AddressNode()
    #     self.link_map(address_node, EdgeBase.TYPE_NORMAL,EntityNode.NODE_ADDRESS)
    #
    # def add_number_node(self):
    #     number_node = NumberNode()
    #     self.link_map(number_node, EdgeBase.TYPE_NORMAL,EntityNode.NODE_NUMBER)
    #
    # def add_special_node(self):
    #     special_node = SpecialNode()
    #     self.link_map(special_node, EdgeBase.TYPE_NORMAL,EntityNode.NODE_SPECIAL)
    #
    # def get_special_node(self)->SpecialNode:
    #     return self.follow_edge_map[EntityNode.NODE_SPECIAL].node_to
    #
    #
    #
    #
    #
    # def get_time_node(self)->TimeNode:
    #     return self.follow_edge_map[EntityNode.NODE_TIME].node_to
    #
    # def get_address_node(self)->AddressNode:
    #     return self.follow_edge_map[EntityNode.NODE_ADDRESS].node_to
    #
    # def get_number_node(self)->NumberNode:
    #     return self.follow_edge_map[EntityNode.NODE_NUMBER].node_to


    def compare(self,node1)->list:
        arr = []
        if(self.get_value()!=node1.get_value()):
            arr.append(CompareValue(EntityNode.COMPARE_UNLIKE,self,node1))
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            node_to = edge.node_to
            node_to2 = node1.get_entity_follow(node_to.get_value(),edge)
            if(node_to2 == None):
                arr.append(CompareValue(NodeBase.COMPARE_LACK,node_to,None,self,node1))
            else:
                arr = arr+node_to.compare(node_to2,self,node1)

        for edge_key in node1.follow_edge_map:
            edge = node1.follow_edge_map[edge_key]
            node_to = edge.node_to
            node_to2 = self.get_entity_follow(node_to.get_value(),edge)
            if(node_to2 == None):
                arr.append(CompareValue(NodeBase.COMPARE_MORE,None,node_to,self,node1))
        return arr

    def get_entity_follow(self,node_value1,edge1):
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            if(edge.type==edge1.type):
                if(edge.node_to.get_value()==node_value1):
                    return edge.node_to
        return None


    # def get_str1(self,n):
    #     head = n*"  "
    #     str1 = head+"EntityNode:"
    #     str1 = str1  + ":" + self.get_value() + "\n"
    #     for key in self.follow_edge_map:
    #         edge = self.follow_edge_map[key]
    #         node_to = edge.node_to
    #         ctr = node_to.get_str1(n+1)
    #         str1 = str1  + head +  ctr + "\n"
    #
    #     for edge in self.edge_list:
    #         node_to = edge.node_to
    #         ctr = node_to.get_str1(n + 1)
    #         str1 = str1 + head + ctr + "\n"
    #
    #     return str1



