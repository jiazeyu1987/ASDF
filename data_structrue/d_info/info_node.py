from . import *
from .. import *
from data_structrue import NodeBase,EdgeBase
class InfoNode(NodeBase):
    def __init__(self):
        super().__init__("")


    def get_head(self):
        return self.get_next_node_by_edge(EdgeBase.TYPE_INFO)

    def add_entity(self,entity_node):
        self.link(entity_node, EdgeBase.TYPE_INFO)

    def add_source(self,str1):
        self.infosource_node = InfoSourceNode()
        self.infosource_node.value = str1
        self.link(self.infosource_node, EdgeBase.TYPE_NORMAL)

    def create_node(self,in_node,node_parent):
        if(in_node.type==NodeBase.TYPE_ENTITY):
            node1 = EntityNode(in_node.get_value())
            self.add_entity(node1)
        elif(in_node.type==NodeBase.TYPE_SPECIAL_CHILD):
            node1 = SpecialChildNode(in_node.get_value())
            print(node_parent.get_value())
        else:
            raise Exception("error create node of in node type:"+in_node.type.__str__())

    def compare_info_node(self,info1):
        cnode1  = self
        cnode2  = info1
        arr = []
        while True:
            if(cnode1!=None):
                cnode1 = cnode1.get_next_node_by_edge(EdgeBase.TYPE_INFO)
            if (cnode2 != None):
                cnode2 = cnode2.get_next_node_by_edge(EdgeBase.TYPE_INFO)


            if(cnode1==None and cnode2==None):
                return arr
            if(cnode1==None):
                arr.append(CompareValue(NodeBase.COMPARE_MORE,None,cnode2,None,cnode2))
                continue
            if(cnode2==None):
                arr.append(CompareValue(NodeBase.COMPARE_LACK, cnode1, None,cnode1,None))
                continue
            else:
                arr = arr+cnode1.compare(cnode2)
                continue



    def get_str1(self,n):
        head = n*"  "
        str1 = head+"InfoNode:\n"
        str1 = str1  + ":" + self.get_value().__str__() + "\n"
        cnode = self.get_next_node_by_edge(EdgeBase.TYPE_INFO)
        while True:
            if(cnode==None):
                break
            str1 = str1 + cnode.get_str1(n+1)+"\n"
            cnode = cnode.get_next_node_by_edge(EdgeBase.TYPE_INFO)
        return str1


    def __str__(self):
        return self.get_str1(0)