from . import *
from .. import *
from data_structrue import NodeBase,EdgeBase

class EntityNodeCompareTool():


    def __init__(self):
        pass


    def compare1(self):
        from .. import SimpleNodeChain,FastChain,FastMap,InfoNode,ValueNode
        from .. import im, vm
        adjlist = ["beauty", "small", "big", "hurge", "smooth", "red", "blue", "strong", "thin"]
        entitylist = ["desk", "hand", "human", "dog", "cat", "chiken", "kitty", "mouse"]

        for entity1 in adjlist:
            for i in range(10):
                chain1 = SimpleNodeChain(["controller"])
                info_node = InfoNode()
                node1 = EntityNode(entity1)
                # beauty_node = SpecialChildNode("beauty")
                # node1.add_special_child_node(beauty_node)
                info_node.add_entity(node1)
                vm.link(chain1,info_node)


        #self.compare_simple_node_chain(chain1,chain2)
        return
        for entity1 in adjlist:
            chain2 = SimpleNodeChain(["beauty", entity1])
            info_node2 = InfoNode()
            node2 = EntityNode("controller")
            info_node2.add_entity(node2)
            beauty_node = SpecialChildNode(adj_word)
            #value_node = ValueNode(ValueNode.VALUE_EXIST_MORE)
            #beauty_node.add_value_node(value_node)
            node2.add_special_child_node(beauty_node)
            vm.link(chain2, info_node2)
            vm.analyse(chain2.get_key(),info_node2)
            # arr = info_node.compare_info_node(info_node2)
            # print(len(arr))
            # for i in arr:
            #     print(i)



    def compare_simple_node_chain(self,chain1:SimpleNodeChain,chain2:SimpleNodeChain):
        from .. import FastMap
        add_weight = 1
        map_compare = FastMap()
        edgelist = self.get_fast_impression(chain1,chain2,map_compare,add_weight)

        while True:
            max_len,node1,node2 = self.get_max_len(chain1,chain2,edgelist,add_weight)
            if(max_len==0):
                break
            tmp_name = NodeBase.create_default_value()
            chain1.change_shape(node1,max_len,tmp_name)
            chain2.change_shape(node2,max_len,tmp_name)
        print(chain1)
        print(chain2)



    def get_max_len(self,chain1:SimpleNodeChain,chain2:SimpleNodeChain,edgelist,add_weight):
        max_node1 = None
        max_node2 = None
        max_chain_len = 0
        while True:
            if (len(edgelist) == 0):
                break
            edge = edgelist.pop(0)
            if (edge == None):
                break
            if (edge.strong > add_weight):
                simple_node, node_to = chain2.location_edge(edge)
                if (simple_node == None):
                    continue
                else:
                    len_chain, node = chain2.find_compare(chain1, simple_node)

                    if(len_chain>max_chain_len):
                        max_chain_len = len_chain
                        max_node1 = node
                        max_node2 = simple_node
                    break
            else:
                continue
        return max_chain_len,max_node1,max_node2

    def get_fast_impression(self,chain1,chain2,map_compare,add_weight):
        from .. import FastChain
        fast_chain1 = FastChain(chain1, map_compare, add_weight)
        fast_chain2 = FastChain(chain2, map_compare, add_weight)
        return fast_chain2.edgelist