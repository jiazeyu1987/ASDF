from data_structrue import NodeBase

class SpecialChildNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.type = NodeBase.TYPE_SPECIAL_CHILD

    def add_value_node(self,node1):
        self.link(node1,NodeBase.TYPE_NORMAL)

    def compare(self,node1,entity1,entity2):
        from .. import CompareValue
        cnode1 = self.get_first_node()
        cnode2 = node1.get_first_node()
        arr = []
        if(self.get_value()!=node1.get_value()):
            arr.append(CompareValue(NodeBase.COMPARE_UNLIKE,self,node1,entity1,entity2))
        elif(cnode1==None):
            arr.append(CompareValue(NodeBase.COMPARE_MORE, None, cnode2,entity1,entity2))
        elif (cnode2 == None):
            arr.append(CompareValue(NodeBase.COMPARE_LACK, cnode1, None,entity1,entity2))
        else:
            arr = arr+cnode1.compare(cnode2,entity1,entity2)
        return arr

    def get_str1(self,n):
        head = n*"  "
        str1 = head+"SpecialChildNode:"
        str1 = str1  + ":" + self.get_value() + "\n"
        for key in self.follow_edge_map:
            edge = self.follow_edge_map[key]
            node_to = edge.node_to
            ctr = node_to.get_str1(n+1)
            str1 = str1  + head +  ctr + "\n"

        for edge in self.edge_list:
            node_to = edge.node_to
            ctr = node_to.get_str1(n + 1)
            str1 = str1 + head + ctr + "\n"
        return str1

