from .. import SimpleNodeChain,SimpleNodeChainNode,SimpleNodeChainEdge
from . import FastNode,FastEdge
import globalconfig as g
class FastChain:
    FAST_CHAIN_ID = 1
    def __init__(self,chain:SimpleNodeChain,map1):
        self.id = FastChain.FAST_CHAIN_ID
        FastChain.FAST_CHAIN_ID+=1
        self.edgelist = []
        self._get_chain(chain,map1)

    def _get_chain(self,chain:SimpleNodeChain,map1):
       current_fast_node = None
       current_chain_node = chain.head
       while True:
           if(current_chain_node!=None):
               char1 = current_chain_node.value
               if (char1 in map1):
                   map1[char1].strong += g.g_fn_add_weight_number
               else:
                   map1[char1] = FastNode(char1)
                   map1[char1].strong += g.g_fn_add_weight_number
               fast_node = map1[char1]
               if(current_fast_node!=None):
                    edge = current_fast_node.add_node(fast_node)
                    self.edgelist.append(edge)
               else:
                   edge = FastEdge(None, fast_node)
                   edge.add_weight()
                   self.edgelist.append(edge)

               current_fast_node = fast_node
               current_chain_node = current_chain_node.get_next_node()
           else:
               break


    def get_fast_compare_result(self):
        chain = SimpleNodeChain()
        simple_current = None
        for edge in self.edgelist:
            node_to = edge.node_to
            if(node_to.is_strong_enough()):
                simple_tmp = SimpleNodeChainNode(node_to.value)
            else:
                simple_tmp = SimpleNodeChainNode(g.replace_symbol)
                if(simple_current!=None and simple_current.value==g.replace_symbol):
                    continue
            if(simple_current==None):
                chain.head = simple_tmp
            else:
                simple_edge = SimpleNodeChainEdge(simple_current, simple_tmp)
                if(simple_current.value!=g.replace_symbol and simple_tmp.value!=g.replace_symbol):
                    simple_edge.strong = edge.strong
                simple_current.add_edge(simple_edge)
            simple_current = simple_tmp
        return chain


    def release_fast_chain(self):
        for edge in self.edgelist:
            node_to = edge.node_to
            node_to.lose_weight()
            edge.lose_weight()


    def __str__(self):
        len1 = len(self.edgelist)
        str1 = "fast chain info:" + len1.__str__() + " "
        for edge in self.edgelist:
            node_to = edge.node_to
            str1 = str1 + " - " + node_to.value
        return str1