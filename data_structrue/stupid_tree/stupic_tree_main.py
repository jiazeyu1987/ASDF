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
            next_node = cnode.get_node(char)
            if(next_node==None):
                return node_arr,len_arr
            nedge = next_node.get_edge(edge)
            if(nedge!=None):
                node_arr.append(nedge.node_to)
                len_arr.append(index)
            cnode = next_node
        return node_arr, len_arr

    def add_value(self,arrlist,final_node,final_edge_type):
        current_node = self.root
        for char in arrlist:
            new_node = current_node.add_node(char)
            current_node = new_node
        current_node.link(final_node,final_edge_type)

    def get_node_by_id(self,node1):
        cnode = self.root
        return cnode.get_node_by_id(node1)

    def get_extra_node(self,nodelist,edge_type):
        cnode = self.root
        for node in nodelist:
            has_flag = False
            for key in cnode.follow_edge_map:
                if(cnode.follow_edge_map[key].node_to.id==node.id):
                    cnode=cnode.follow_edge_map[key].node_to
                    has_flag = True
                    break
            if(has_flag==False):
                return None
        eedge = cnode.get_edge(edge_type)
        if(eedge!=None):
            return eedge.node_to
        return None

    def get_model(self,nodelist,edge):
        return self._get_model(nodelist,edge,self.root)

    def _get_model(self,nodelist,edge,tree_current_node):
        if(len(nodelist)==0):
            nedge = tree_current_node.get_edge(edge)
            if (nedge != None):
                return True,[[]]
        node = nodelist[0]
        oknodes = tree_current_node.get_node_with_replace_nodes(node.get_value())
        if(len(oknodes)==0):
            return False,None
        else:
            alllist = []
            has_flag = False
            for node1 in oknodes:
                r,list1 = self._get_model(nodelist[1:],edge,node1)
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
            new_node = current_node.add_node(char)
            current_node = new_node
        current_node.link(final_node, final_edge_type)

        # uni.unique = True
    def add_chain(self,chain:SimpleNodeChain):
        head = chain.get_head()
        current_node = self.root
        while True:
            head = head.get_next_node()
            if(head==None):
                break
            new_node = current_node.add_node(head.get_value())
            current_node = new_node



    def get_nearest(self,value1):
        return self.root.get_nearest(value1)




    def say(self):
        self.root.say()