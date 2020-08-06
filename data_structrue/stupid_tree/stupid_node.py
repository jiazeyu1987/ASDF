from .. import NodeBase,EdgeBase
import  globalconfig as g
class StupidNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.unique = False
        self.follow_edge_map = {}

    def get_node(self,char):
        if(char in self.follow_edge_map):
            return self.follow_edge_map[char].node_to
        else:
            return None

    def get_node_with_replace_nodes(self,char):
        arr = []
        if(char in self.follow_edge_map):
            arr.append(self.follow_edge_map[char].node_to)
        for key in self.follow_edge_map:
            if(key[0]=="瓛"):
                arr.append(self.follow_edge_map[key].node_to)
        return arr


    def add_node(self,char1):
        from .stupid_edge import StupidEdge
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            if(edge.node_to.get_value()==char1):
                edge.add_stupid_weight()
                return edge.node_to
            else:
                pass
        node_new = StupidNode(char1)
        edge = StupidEdge(self,node_new)
        edge.add_stupid_weight()
        self.follow_edge_map[char1] = edge
        return node_new

    def add_action(self,action,node,entity_node):
        node1 = self.get_action_node(action)
        edge_weight1 = self.link(node1,EdgeBase.TYPE_LINK_ACTION)

        node2 = node1.get_node_by_edgetype_in_edgelist(node.get_value(),EdgeBase.TYPE_LINK_ACTION)
        if(node2==None):
            node2 = node.copy()
        edge_weight2 = node1.link(node2, EdgeBase.TYPE_LINK_ACTION)

        edge_weight3 = 0
        if(entity_node!=None):
            node3 = node2.get_node_by_edgetype_in_edgelist(entity_node.get_value(), EdgeBase.TYPE_LINK_ACTION)
            if (node3 == None):
                node3 = entity_node.copy()
            edge_weight3 = node2.link(node3, EdgeBase.TYPE_LINK_ACTION)
        print(edge_weight1,edge_weight2,edge_weight3)

    def get_action_node(self,action):
        node1 = self.get_node_by_edgetype_in_edgelist(action,EdgeBase.TYPE_LINK_ACTION)
        if(node1==None):
            node1=NodeBase(action)
        else:
            pass
        return node1

    def get_one1_action(self):
        for edge in self.edge_list:
            if(edge.type == EdgeBase.TYPE_LINK_ACTION):
                return edge
        return None

    def get_nearest(self,value1,depth=1):
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            node_to = edge.node_to
            if(node_to.get_value()==value1):
                return node_to,depth

        min_depth = 99999
        min_node = None
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            node_to = edge.node_to
            node_v,new_depth = node_to.get_nearest(value1,depth+1)
            if(new_depth<min_depth):
                min_depth = new_depth
                min_node = node_v
        return min_node,min_depth

    def get_map_str1(self,n):
        head = n*"  "
        str1 = head
        str1 = str1  + ":" + self.get_value() + "\n"
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            str1 = str1 + (n+1)*"  " +" "+ edge.strong.__str__()+"\n"
            node_to = edge.node_to
            str1 = str1 + node_to.get_map_str1(n+1) + "\n"

        for edge in self.edge_list:

            if(edge.type != EdgeBase.TYPE_WORD_TO_NODE):
                continue
            node_to = edge.node_to
            str1 = str1 + node_to.get_str1(n + 1,[EdgeBase.TYPE_NORMAL]) + "\n"
        return str1


    def say(self):
        print(self.get_map_str1(0))