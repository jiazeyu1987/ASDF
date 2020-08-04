class NodeBase:
    TYPE_NORMAL = "TYPE_NORMAL"
    TYPE_TIME = "TYPE_TIME"
    TYPE_ADDRESS = "TYPE_ADDRESS"
    TYPE_NUMBER = "TYPE_NUMBER"
    TYPE_SPECIAL = "TYPE_SPECIAL"
    TYPE_SPECIAL_CHILD = "TYPE_SPECIAL_CHILD"
    TYPE_INFO_SOURCE = "TYPE_INFO_SOURCE"
    TYPE_VALUE = "TYPE_VALUE"
    TYPE_ENTITY = "TYPE_ENTITY"
    TYPE_REPLACE = "TYPE_REPLACE"

    COMPARE_MORE = "more"
    COMPARE_LACK = "lack"
    COMPARE_UNLIKE = "unlike"

    ACTION_CREATE = "action_create_J"
    NODE_BASE_ID = 1

    VALUE_REPLACE = "籴Replace"
    def __init__(self,value:str,strong=0):
        self._value = value
        self.strong = 0
        self.type = 0
        #self.follow_edge_map = {}
        self.edge_list = []
        self.id = NodeBase.NODE_BASE_ID
        NodeBase.NODE_BASE_ID+=1


    def get_edge_list(self):
        return self.edge_list

    def copy(self):
        node = NodeBase(self.get_value())
        node.strong = self.strong
        node.type = self.type
        return node

    def get_next_node_by_edge(self,edge_type):
        for edge in self.edge_list:
            if(edge.type == edge_type):
                return edge.node_to
        return None

    @staticmethod
    def create_default_value()->str:
        return "摭"+NodeBase.NODE_BASE_ID.__str__()

    def add_weight(self,weight):
        self.strong+=weight

    def lose_weight(self,weight):
        self.strong-=weight

    def get_value(self)->str:
        return self._value.__str__()

    def link(self,node,edge_type):
        from .edge_base import EdgeBase
        if(node.get_value()==self.get_value()):
            raise Exception(node.get_value())

        for edge in self.edge_list:
            node_to = edge.node_to
            if(node_to.get_value()==node.get_value() and edge.type == edge_type):
                edge.add_weight(1)
                node_to.add_weight(1)
                return edge.strong
        edge = EdgeBase(self, node)
        edge.type = edge_type
        edge.add_weight(1)
        self.edge_list.append(edge)
        return edge.strong

    def get_node_by_edgetype_in_edgelist(self,value1,type):
        for edge in self.edge_list:
            node_to = edge.node_to
            if(edge.type==type and node_to.get_value()==value1):
                return node_to
        return None

    def add_voice_child(self,entity_node,edge_type):
        self.link(entity_node,edge_type)

    def get_voice_child(self,entity_node,edge_type):
        for edge in self.edge_list:
            node_to = edge.node_to
            if(node_to.equal_node(entity_node)):
                return node_to
        return None

    def add_voice_child_weight(self,child):
        for edge in self.edge_list:
            node_to = edge.node_to
            if(node_to==child):
                edge.add_weight(1)
                node_to.add_weight(1)
                return

    def equal_node(self,node1,depth = 0):
        if(self.get_value()!=node1.get_value()):
            return False
        if(len(self.edge_list)!=len(node1.edge_list)):
            return False
        if(depth<10):
            for i in range(len(self.edge_list)):
                edge  = self.edge_list[i]
                edge1 = node1.edge_list[i]
                if(edge.node_to.equal_node(edge1.node_to,depth+1)==False):
                    return False
        return True

    def link_map(self,node,edge_type,key):
        from .edge_base import EdgeBase
        edge = None
        if(edge_type==EdgeBase.TYPE_NORMAL):
            edge = EdgeBase(self,node)
        else:
            raise Exception("lakdsjflsakdfjlskfdj")
        if(key in self.follow_edge_map):
            self.follow_edge_map[key].add_weight(1)
        else:
            self.follow_edge_map[key] = edge

    def get_strongest_edge(self):
        max_edge = None
        max_strong = -1
        for key in self.follow_edge_map:
            edge = self.follow_edge_map[key]
            if(edge.strong>max_strong):
                max_edge = edge
        return max_edge

    def get_first_node(self):
        if(len(self.edge_list)==0):
            return None
        else:
            return self.edge_list[0].node_to

    def get_str1(self, n):
        from . import EdgeBase
        head = n * "  "
        str1 = head
        str1 = str1 + self.get_value() + "\n"
        #print(self._value)
        for edge in self.edge_list:
            if(edge.type in [EdgeBase.TYPE_BELONG]):
                continue
            #print("1",self._value,edge.type,edge.node_to.get_value())
            node_to = edge.node_to
            str1 = str1+head+node_to.get_str1(n+1)


        return str1

    def __str__(self):
        return self.get_str1(0)