from . import *
class NodeBase:
    TYPE_NORMAL = "TYPE_NORMAL"
    TYPE_TIME = "TYPE_TIME"
    TYPE_ADDRESS = "TYPE_ADDRESS"
    TYPE_NUMBER = "TYPE_NUMBER"
    TYPE_SPECIAL = "TYPE_SPECIAL"
    TYPE_CHILD = "TYPE_CHILD"
    TYPE_INFO_SOURCE = "TYPE_INFO_SOURCE"
    TYPE_VALUE = "TYPE_VALUE"
    TYPE_ENTITY = "TYPE_ENTITY"
    TYPE_REPLACE = "TYPE_REPLACE"

    COMPARE_MORE = "more"
    COMPARE_LACK = "lack"
    COMPARE_UNLIKE = "unlike"

    ACTION_CREATE = "action_create_J"
    NODE_BASE_ID = 1

    VALUE_REPLACE = "瓛"
    all_map = {}
    def __init__(self,value:str,flag,strong=0):
        if(flag!="lfljaskdfj"):
            raise Exception("ffffff")
        self._value = value
        self._weight = 0
        self.type = "base"
        self.edge_list = []
        self.id = NodeBase.NODE_BASE_ID
        NodeBase.NODE_BASE_ID+=1

        #for stupid tree
        self.follow_edge_map = {}


    # 返回基础节点的复制引用
    @staticmethod
    def create_node(value):
        if(value in NodeBase.all_map):
            pass
        else:
            NodeBase.all_map[value] = NodeBase(value,"lfljaskdfj")
        node1 = NodeBase.all_map[value]
        nc = NodeBase(value,"lfljaskdfj")
        nc.type = node1.type
        nc._weight = node1._weight
        nc.type = "child"
        node1.link(nc, EdgeBase.TYPE_CHILD,1)
        return nc

    # 获取基础节点
    def get_base_node(self):
        if (self._value in NodeBase.all_map):
            pass
        else:
            NodeBase.all_map[self._value] = NodeBase(self._value, "lfljaskdfj")
        node1 = NodeBase.all_map[self._value]
        return node1

    # 当更换节点的时候会用到
    def replace_node(self,val1):
        base_node = self.get_base_node()
        base_node.unlink(self)

        self._value = val1
        base_node = self.get_base_node()
        base_node.link(self,NodeBase.TYPE_CHILD,1)

    # 断开自己与目标节点的连接
    def unlink(self,node1):
        for edge in self.edge_list:
            if(edge.node_to.id == node1.id):
                self.edge_list.remove(edge)
                return True
        return False

    # 判断自己是否有指定类型的edge
    def has_edge(self, edge_type):
        for edge in self.edge_list:
            if (edge.type == edge_type):
                return True
        return False


    # 获取指定类型的一条edge
    def get_1edge(self, edge_type):
        for edge in self.edge_list:
            if (edge.type == edge_type):
                return edge
        return None

    # 获取指定类型的一条edge的一个child
    def get_1node(self,edge_type=EdgeBase.TYPE_NORMAL):
        from . import EdgeBase
        for edge in self.edge_list:
            if(edge.type!=edge_type):
                continue
            return edge.node_to

    # 获取自己备份的一个copy节点
    def copy(self):
        node = NodeBase.create_node(self.get_value())
        node._weight = self._weight
        node.type = self.type
        return node



    # 加权重
    def add_weight(self,weight):
        self._weight+=weight

    # 减权重
    def lose_weight(self,weight):
        self._weight-=weight

    def get_value(self)->str:
        return self._value.__str__()

    # 除非特殊原因，不能用基点连接基点，不能自己连接自己
    def link(self,node,edge_type,type=2):
        if(type==2):
            if(self.type=="base"):
                raise Exception("can't use base1")
            if (node.type == "base"):
                raise Exception("can't use base2")
            if(node.id==self.id):
                raise Exception(node.get_value())

        edge = EdgeBase(self, node)
        edge.type = edge_type
        edge.add_weight(1)
        self.edge_list.append(edge)
        return edge._weight

    # 通过节点内容与edge类型来唯一确认一个节点
    def get_node(self,node_value,edge_type):
        for edge in self.edge_list:
            node_to = edge.node_to
            if(edge.type==edge_type and node_to.get_value()==node_value):
                return node_to
        return None

    
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
            if(edge._weight>max_strong):
                max_edge = edge
        return max_edge

    def get_first_node(self):
        if(len(self.edge_list)==0):
            return None
        else:
            return self.edge_list[0].node_to


    def get_node_by_edge_type(self,edge_type):
        arr = []
        for edge in self.edge_list:
            if(edge.type == edge_type):
                arr.append(edge.node_to)
        return arr

    def get_str1(self, n,edgelist,edgetype=""):
        from . import EdgeBase
        head = n * "        "
        str1 = ""
        str1 = str1 + head+self.type+","+self.get_value() + "\n"
        #print(self._value)
        for edge in self.edge_list:
            if((edge.type in edgelist) == False):
                continue
            #print("1",self._value,edge.type,edge.node_to.get_value())
            node_to = edge.node_to
            str1 = str1+head+node_to.get_str1(n+1,edgelist,edge.type)


        return str1

    def get_all_reffer_nodes(self):
        arr = []
        base_node = self.get_base_node()
        for edge in base_node.edge_list:
            if(edge.type == EdgeBase.TYPE_CHILD):
                arr.append(edge.node_to)
        return arr


    def contain(self,node1):
        from . import EdgeBase
        sub_nodes = self.get_all_reffer_nodes()
        for node in sub_nodes:
            for edge in node.edge_list:
                if(edge.type == EdgeBase.TYPE_CONTAIN):
                    node_to = edge.node_to
                    if(node1.get_value()==node_to.get_value()):
                        return node_to
        return None

    def copy_model(self,edgelist):
        from . import EdgeBase
        node1 = self.copy()
        for edge in self.edge_list:
            if(edge.type in edgelist):
                node_to = edge.node_to.copy_model(edgelist)
                node1.link(node_to,edge.type)
        return node1

    def __str__(self):
        from . import EdgeBase
        return self.get_str1(0,[EdgeBase.TYPE_NORMAL])

    def print(self,edgelist):
        print(self.get_str1(0,edgelist))




    def print_base(self,edgelist):
        str1 = "base_node info:" + self.get_value() + " " + "\n"
        nodes = self.get_all_reffer_nodes()
        for node in nodes:
            str1 = str1 + "" + node.type + node.id.__str__() + "\n"
            for edge in node.edge_list:
                if((edge.type in edgelist) == False):
                    continue
                node_to = edge.node_to
                str1 = str1+""+node_to.get_str1(1,edgelist,edge.type)
        print(str1)













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
        from . import EdgeBase
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            if(edge.node_to.get_value()==char1):
                return edge.node_to
            else:
                pass
        node_new = NodeBase.create_node(char1)
        edge = EdgeBase(self,node_new)
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

    def get_node_by_id(self,node1):
        for key in self.follow_edge_map:
            node_to = self.follow_edge_map[key].node_to
            if (node_to.id == node1.id):
                return node_to
            else:
                if(node_to.get_node_by_id(node1)!=None):
                    return node_to.get_node_by_id(node1)
        return None

    def get_map_str1(self,n):
        head = n*"  "
        str1 = head
        str1 = str1  + ":" + self.get_value() + "\n"
        for edge_key in self.follow_edge_map:
            edge = self.follow_edge_map[edge_key]
            str1 = str1 + (n+1)*"  " +" "+ edge._weight.__str__()+"\n"
            node_to = edge.node_to
            str1 = str1 + node_to.get_map_str1(n+1) + "\n"

        for edge in self.edge_list:

            if(edge.type != EdgeBase.TYPE_NODE_TO_MODEL):
                continue
            node_to = edge.node_to
            str1 = str1 + node_to.get_str1(n + 1,[EdgeBase.TYPE_NORMAL]) + "\n"
        return str1


    def add_node_by_value(self,node1):
        if(node1.get_value()==self._value):
            raise Exception(node1.get_value())
        self.current_node.link(node1,EdgeBase.TYPE_CONTAIN)
        node1.link(self,EdgeBase.TYPE_BELONG)

    def say(self):
        print(self.get_map_str1(0))