from .. import *
from ..simple_node_chain import SimpleNodeChain
from . import *
class FastTree:
    def __init__(self):
        self.root = FastNode("")


    #add node weight not edge weight
    def add_simple_node_chain(self,chain:SimpleNodeChain):
        target_node = chain.head
        while True:
            if(target_node==None):
                break
            self.link_target(target_node)
            follow_edge = target_node.follow_edge
            if(follow_edge==None):
                break
            target_node = follow_edge.node_to


    def link_target(self,target_node:SimpleNodeChainNode):
        fast_edge = FastEdge(self.root, target_node)
        self.root.add_edge(fast_edge)