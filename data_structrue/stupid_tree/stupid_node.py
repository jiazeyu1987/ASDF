from .. import NodeBase
import  globalconfig as g
class StupidNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge_map = {}
        self.strong = 0
        self.unique = False


    def add_node(self,char1):
        from .stupid_edge import StupidEdge
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            if(edge.node_to.value==char1):
                edge.add_stupid_weight()
                return edge.node_to
            else:
                pass
        node_new = StupidNode(char1)
        edge = StupidEdge(self,node_new)
        edge.add_stupid_weight()
        self.follow_edge_map[char1] = edge
        return node_new


    def get_str1(self,n):
        head = n*"  "
        str1 = head
        str1 = str1  + ":" + self.value + "\n"
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            str1 = str1 + (n+1)*"  " +" "+ edge.strong.__str__()+"\n"
            node_to = edge.node_to
            str1 = str1 + node_to.get_str1(n+1) + "\n"
        return str1

    def say(self):
        print(self.get_str1(0))