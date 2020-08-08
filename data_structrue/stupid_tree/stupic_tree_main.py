from . import *
from .. import *
import globalconfig as g
class StupidTree:
    def __init__(self):
        self.root = NodeBase.create_node("擱")

    def get_linked_node_by_strlist(self,strlist,edge):
        cnode = self.root
        index = 0
        node_arr = []
        len_arr = []

        for i in range(len(strlist)):
            char = strlist[i]
            index+=1
            #next_node = cnode.link(NodeBase.create_node(char),EdgeBase.TYPE_NORMAL,True)
            next_node = cnode.get_1node(EdgeBase.TYPE_NORMAL,char)
            if(next_node==None):
                return node_arr,len_arr
            nedge = next_node.get_1edge(edge)
            if(nedge!=None):
                node_arr.append(nedge.node_to)
                len_arr.append(index)
            cnode = next_node
        return node_arr, len_arr

    def add_value(self,arrlist,final_node,final_edge_type):
        current_node = self.root
        for char in arrlist:
            new_node = current_node.link(NodeBase.create_node(char),EdgeBase.TYPE_NORMAL,True)
            current_node = new_node
        current_node.link(final_node,final_edge_type)

    def get_node_by_id(self,node1):
        cnode = self.root
        return cnode.get_1node_by_id(node1.id)

    def get_extra_node(self,nodelist,edge_type):
        cnode = self.root
        for node in nodelist:
            has_flag = False
            for edge in cnode.edge_list:
                node_to = edge.node_to
                key = node_to.get_value()
                if(node_to.id==node.id):
                    cnode=node_to
                    has_flag = True
                    break
            if(has_flag==False):
                return None
        eedge = cnode.get_1edge(edge_type)
        if(eedge!=None):
            return eedge.node_to
        return None



    def get_model(self,nodelist):
        return self._get_model(nodelist,self.root)

    def _get_model(self,nodelist,tree_current_node):
        if(len(nodelist)==0):
            nedge = tree_current_node.get_1edge(EdgeBase.TYPE_REFFER)
            if (nedge != None):
                return True,[[]]
        node = nodelist[0]
        oknodes = tree_current_node.get_allnode_with_startchar(node.get_value(),NodeBase.VALUE_REPLACE)
        if(len(oknodes)==0):
            return False,None
        else:
            alllist = []
            has_flag = False
            for node1 in oknodes:
                r,list1 = self._get_model(nodelist[1:],node1)
                if(r):
                    has_flag = True
                    for listsub in list1:
                        newlist = [node1]+listsub
                        alllist.append(newlist)
            if(has_flag):
                return True,alllist
            else:
                return False,None

    def add_models(self,nodelist,final_node,final_edge_type):
        current_node = self.root
        for node in nodelist:
            char = node.get_value()
            new_node = current_node.link(NodeBase.create_node(char),EdgeBase.TYPE_NORMAL,True)
            current_node = new_node
        current_node.link(final_node, final_edge_type)




    def get_nearest(self,value1):
        return self.root.get_nearest(value1)




    def say(self):
        self.root.print_map()