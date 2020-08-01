from .. import SimpleNodeChain,SimpleNodeChainNode,SimpleNodeChainEdge
from . import FastNode,FastEdge,FastMap
import globalconfig as g
class FastChain:
    FAST_CHAIN_ID = 1
    def __init__(self,chain:SimpleNodeChain,map1:FastMap,add_weight = g.g_fn_add_weight_number):
        self.id = FastChain.FAST_CHAIN_ID
        FastChain.FAST_CHAIN_ID+=1
        self.edgelist = []
        self.repeat_node_chain = SimpleNodeChain()
        self._get_chain(chain,map1,add_weight)

    def _get_chain(self,chain:SimpleNodeChain,map1:FastMap,add_weight):
       current_fast_node = None
       current_chain_node = chain.head
       has_repeat_flag = False
       while True:
           if(current_chain_node!=None):
               char1 = current_chain_node.get_value()
               if (char1 in map1.get_map()):
                   map1.get_map()[char1].strong += add_weight
               else:
                   map1.get_map()[char1] = FastNode(char1)
                   map1.get_map()[char1].strong += add_weight
               fast_node = map1.get_map()[char1]
               if(current_fast_node!=None):
                    edge,flag = current_fast_node.add_node(fast_node,add_weight)
                    self.edgelist.append(edge)
                    if(flag):
                        has_repeat_flag = True
                        if(self.repeat_node_chain.head==None or self.repeat_node_chain.current_node.value==g.replace_symbol):
                            self.repeat_node_chain.enter_node_val(current_fast_node.value)
                        self.repeat_node_chain.enter_node_val(fast_node.value)
                    else:
                        if(fast_node.strong>add_weight):
                            has_repeat_flag = True
                            self.repeat_node_chain.add_zhanwei_node()
                            self.repeat_node_chain.enter_node_val(fast_node.value)
                        else:
                            self.repeat_node_chain.add_zhanwei_node()
               else:
                   if (fast_node.strong > add_weight):
                       has_repeat_flag = True
                       self.repeat_node_chain.add_zhanwei_node()
                       self.repeat_node_chain.enter_node_val(fast_node.value)
                   else:
                       edge = FastEdge(None, fast_node)
                       edge.add_weight(add_weight)
                       self.edgelist.append(edge)

               current_fast_node = fast_node
               current_chain_node = current_chain_node.get_next_node()
           else:
               break

       if(has_repeat_flag==False):
           self.repeat_node_chain = None






    def compare(self,chain:SimpleNodeChain,map1:FastMap):
        current_fast_node = None
        current_chain_node = chain.head
        arr = []
        rev = -1
        has_flag = False
        edge1 = None
        str1 = ""
        while True:
            if (current_chain_node != None):
                char1 = current_chain_node.value
                if (char1 in map1.get_map()):
                    pass
                else:
                    map1.get_map()[char1] = FastNode(char1)
                fast_node = map1.get_map()[char1]
                if (current_fast_node != None):
                    edge, flag = current_fast_node.add_node(fast_node, 0)
                    edge1 = edge
                    if (flag):
                        has_flag = True
                        if(rev==-1):
                            rev = 1
                            str1 = str1 + edge.node_from.value
                        elif(rev==0):
                            arr.append([str1,0])
                            str1 = edge.node_from.value
                            rev = 1
                        else:
                            str1 = str1+edge.node_from.value
                    else:
                        if(rev==-1):
                            rev = 0
                            str1 = str1+edge.node_from.value
                        elif (rev == 1):
                            str1 = str1 + edge.node_from.value
                            arr.append([str1, 1])
                            str1 = ""
                            rev = 0
                        else:
                            str1 = str1 + edge.node_from.value
                else:
                    pass
                current_fast_node = fast_node
                current_chain_node = current_chain_node.get_next_node()
            else:
                if (rev == 1):
                    str1 = str1+edge1.node_to.value
                    arr.append([str1, 1])
                else:
                    str1 = str1 + edge1.node_to.value
                    arr.append([str1, 0])
                break
        return arr,has_flag

    def release_fast_chain(self):
        for edge in self.edgelist:
            node_to = edge.node_to
            node_to.lose_weight()
            edge.lose_weight()


    def print_edgelist(self):
        for edge in self.edgelist:
            print("fast_chain_edge",edge.strong.__str__(),edge.node_to.value)

    def __str__(self):
        len1 = len(self.edgelist)
        str1 = "fast chain info:" + len1.__str__() + " "
        for edge in self.edgelist:
            node_to = edge.node_to
            str1 = str1 + " - " + node_to.value
        return str1