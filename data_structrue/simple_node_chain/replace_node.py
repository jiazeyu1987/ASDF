from . import *
from .. import *
class ReplaceNode(SimpleNodeChainNode):
    def __init__(self):
        super().__init__("")
        self._value = "瓛"+self.id.__str__()
        self.current_node = self

    def add_node_by_value(self,node1):
        if(node1.get_value()==self._value):
            raise Exception(node1.get_value())
        self.current_node.link(node1,EdgeBase.TYPE_CONTAIN)
        node1.link(self,EdgeBase.TYPE_BELONG)


    def get_str2(self, n):
        from . import EdgeBase
        head = n * "  "
        str1 = head
        str1 = str1 + self.get_value() + "\n"
        #print(self._value)
        for edge in self.edge_list:
            if (edge.type != EdgeBase.TYPE_CONTAIN):
                continue
            #print("1",self._value,edge.type,edge.node_to.get_value())
            node_to = edge.node_to
            str1 = str1+head+node_to.get_str1(n+1)
        return str1



    def print_replace(self):
        print(self.get_str2(0))


