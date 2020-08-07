from . import *
import globalconfig as g
class SimpleNodeChain:
    def __init__(self,list1:list=None):
        self.head = NodeBase.create_node("媫Start")
        #current node
        self.current_node = self.head
        if(list1!=None):
            self.enter_node_list(list1)

    def get_head(self)->SimpleNodeChainNode:
        return self.head


    def get_node_list(self):
        cnode = self.get_head()
        arr = []
        while True:
            cnode = cnode.get_1node()
            if(cnode==None):
                return arr
            else:
                arr.append(cnode)

    def add_node(self,new_node:SimpleNodeChainNode):
        self.current_node.link(new_node,EdgeBase.TYPE_NORMAL)
        self.current_node = new_node

    def change_shape(self,node1:SimpleNodeChainNode,len1:int,replace_value:str):
        replace_node = ReplaceNode(replace_value)
        cnode = self.get_head()
        index = -1
        if(cnode==node1):
            edge = SimpleNodeChainEdge(replace_node, cnode)
            replace_node.replace_edge = edge
            self.head = replace_node
            index = 0
        while True:
            if(cnode==None):
                break
            next_node = cnode.get_1node()
            if(index!=-1):
                index+=1
                if(index==len1):
                    cnode.remove_edge()
                    new_edge = SimpleNodeChainEdge(replace_node, next_node)
                    replace_node.edge_list.append(new_edge)
            if(next_node==node1):
                cnode.replace_next_node(replace_node)
                index=0
            cnode = next_node


    def find_compare(self,other_chain,start_node=None):
        cnode = start_node
        if(start_node==None):
            cnode = self.head

        tnode = other_chain.get_head()
        max = 0
        target_node = None
        while True:
            if(tnode.get_value()==cnode.get_value()):
                rn = self.equal_chain_len(cnode,tnode)
                if(cnode.get_value()=="hurge3"):
                    print("FFFFFFFFFFFFFF",cnode.get_value(),t_node.value(),rn)
                if(rn>max):
                    max = rn
                    target_node = tnode

            tnode = tnode.get_1node()
            if(tnode==None):
                break
        return max,target_node

    def equal_chain_len(self,start_node,start_node2):
        index = 0
        cnode = start_node
        tnode = start_node2
        while True:
            if (cnode.get_value() != tnode.get_value()):
                return index
            index+=1
            cnode = cnode.get_1node()
            tnode = tnode.get_1node()
            if(cnode==None or tnode==None):
                return index


    def location_edge(self,edge):
        cnode = self.get_head()
        while True:
            if(cnode==None):
                break
            next_node = cnode.get_1node()
            if(next_node == None):
                break

            nf = cnode.get_value()==edge.node_from.get_value()
            tf = next_node.get_value()==edge.node_to.get_value()
            if(nf and tf):
                return cnode,next_node
            cnode = next_node
        return None,None

    def add_zhanwei_node(self):
        from .. import EdgeBase
        if(self.head==None):
            self.head = SimpleNodeChainNode(g.replace_symbol)
            self.current_node = self.head
        else:
            if(self.current_node.get_value() == g.replace_symbol):
                return
            else:
                new_node = self.new(g.replace_symbol)
                self.current_node.link(new_node,EdgeBase.TYPE_NORMAL)
                self.current_node = new_node


    def compare(self,chain1):
        from .. import FastChain
        map_compare = {}
        fast_chain = FastChain(self, map_compare, 5)
        fast_chain1 = FastChain(chain1, map_compare, 5)
        edgelist = fast_chain.edgelist
        edgelist1 = fast_chain1.edgelist
        print(fast_chain1.repeat_node_chain)
        # e_arr = []
        # for edge in edgelist:
        #     if(edge.strong>5 and edge in edgelist1):
        #         e_arr.append(edge)





    #从receiver/eye异步接收到的数据
    def add_nodes_by_charlist(self,charlist):
        for char1 in charlist:
            self.add_new_node_by_char(char1)


    def __str__(self):
        str1 = "simple node chain info:"
        tmp_node = self.head
        index = 1
        while True:
            if (tmp_node == None):
                break
            if (index > 50):
                break
            index += 1
            str1 = str1 + tmp_node.get_value() + " - "
            if (tmp_node.get_1node() == None):
                break
            tmp_node = tmp_node.get_1node()
        return str1

    def enter_node_list(self,vallist:list):
        for i in range(len(vallist)):
            self.add_new_node_by_char(vallist[i])

    def add_new_node_by_char(self,val):
        from .. import EdgeBase
        if(self.head==None):
            self.head = self.new(val)
            self.current_node = self.head
        else:
            new_node = self.new(val)
            self.current_node.link(new_node,EdgeBase.TYPE_NORMAL)
            self.current_node = new_node



    def get_str(self):
        current = self.get_head()
        str1 = ""
        while True:
            if current==None:
                break
            str1 = str1+current.get_value()
            current = current.get_1node()
        return str1

    def get_key(self):
        current = self.get_head()
        str1 = ""
        arr = []
        while True:
            if current == None:
                break
            str1 = str1 + current.get_value()
            arr.append(current.get_value())
            current = current.get_1node()
        return arr






    def new(self,val):
        return SimpleNodeChainNode(val)

