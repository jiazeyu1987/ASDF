from . import *
from .. import *
from data_structrue import NodeBase,EdgeBase

class EntityNodeCompareTool():


    def __init__(self):
        pass


    def compare1(self):
        #self.compare_x()
        #self.compare_y()
        self.compare_z()
        self.compare_z()

    def compare_z(self):
        from .. import im
        strlist1 = ["房", "子",  "非","常", "美"]
        strlist2 = ["西", "瓜",  "非","常", "美"]
        strlist3 = ["空", "调",  "非","常", "美"]
        strlist4 = ["电", "脑",  "非","常", "美"]
        strlist5 = ["手", "机",  "非","常", "美"]
        biglist = [strlist1,strlist2,strlist3,strlist4,strlist5]
        bigentitylist = []
        self.create_false_entitylist(biglist,bigentitylist)
        for i in range(len(biglist)):
            strlist = biglist[i]
            entity_node = bigentitylist[i]
            im.on_raw_data(strlist,entity_node)
        print("====================")
        strlist1 = ["房", "子",  "非","常", "美"]
        strlist2 = ["房", "子",  "非","常", "小"]
        strlist3 = ["房", "子",  "非","常", "胖"]
        strlist4 = ["房", "子",  "非","常", "大"]
        strlist5 = ["房", "子",  "非","常", "脏"]
        biglist = [strlist1, strlist2, strlist3, strlist4, strlist5]
        bigentitylist = []
        self.create_false_entitylist(biglist, bigentitylist)
        for i in range(len(biglist)):
            strlist = biglist[i]
            entity_node = bigentitylist[i]
            im.on_raw_data(strlist, entity_node)
        print("====================")
        strlist1 = ["房", "子", "非","常", "美"]
        strlist2 = ["房", "子", "特","别","美"]
        strlist3 = ["房", "子", "尤","其", "美"]
        strlist4 = ["房", "子", "有","点", "美"]
        strlist5 = ["房", "子", "及","其", "美"]
        biglist = [strlist1, strlist2, strlist3, strlist4, strlist5]
        bigentitylist = []
        self.create_false_entitylist(biglist, bigentitylist)
        for i in range(len(biglist)):
            strlist = biglist[i]
            entity_node = bigentitylist[i]
            im.on_raw_data(strlist, entity_node)

        # print("====================")
        # strlist1 = ["房", "子", "非", "常", "美"]
        # strlist2 = ["房", "子", "特", "别", "美"]
        # strlist3 = ["房", "子", "尤", "其", "美"]
        # strlist4 = ["房", "子", "有", "点", "美"]
        # strlist5 = ["房", "子", "及", "其", "美"]
        # biglist = [strlist1, strlist2, strlist3, strlist4, strlist5]
        # bigentitylist = []
        # self.create_false_entitylist(biglist, bigentitylist)
        # for i in range(len(biglist)):
        #     strlist = biglist[i]
        #     entity_node = bigentitylist[i]
        #     im.on_raw_data(strlist, entity_node)
        #im.str_tree.say()
        #im.model_node_tree.say()

    def create_false_entitylist(self,biglist,bigentitylist):
        for strlist in biglist:
            str_name = strlist[0]+strlist[1]
            adj = strlist[4]
            vb = strlist[2]+strlist[3]
            node1 = NodeBase.create_node(str_name)
            adj_node = NodeBase.create_node(adj)
            vb_node = NodeBase.create_node(vb)
            node1.link(adj_node,EdgeBase.TYPE_NORMAL)
            adj_node.link(vb_node,EdgeBase.TYPE_NORMAL)
            bigentitylist.append(node1)

    def compare_y(self):
        from .. import im,mt
        node1 = NodeBase.create_node("hand1")
        beauty_node = NodeBase.create_node("hurge")
        value_node = NodeBase.create_node(ValueNode.VALUE_EXIST_MORE)
        value_node2 = NodeBase.create_node(ValueNode.VALUE_EXIST)

        node1.link(beauty_node, EdgeBase.TYPE_NORMAL)
        beauty_node.link(value_node, EdgeBase.TYPE_NORMAL)
        value_node.link(value_node2, EdgeBase.TYPE_NORMAL)



        node2 = EntityNode("hand")
        beauty_node = SpecialChildNode("hurge")
        value_node = ValueNode(ValueNode.VALUE_EXIST_MAX)
        value_node2 = ValueNode(ValueNode.VALUE_EXIST)

        node2.link(beauty_node,EdgeBase.TYPE_NORMAL)
        beauty_node.link(value_node, EdgeBase.TYPE_NORMAL)
        value_node.link(value_node2,EdgeBase.TYPE_NORMAL)



        chain1 = SimpleNodeChain()
        chain1.add_nodes_by_charlist(["hurge","hand1",ValueNode.VALUE_EXIST_MORE,10])
        chain2 = SimpleNodeChain()
        chain2.add_nodes_by_charlist(["hurge","hand",ValueNode.VALUE_EXIST_MAX,10])
        im.on_enter_node(chain1, node1)
        im.on_enter_node(chain2, node2)





    def print_compared_chain(self,chain1, chain2, map1):
        cnode = chain1.get_head()
        while True:
            if (cnode == None):
                break
            if (cnode.id in map1):
                cnode = cnode.get_next_node()
            else:
                print("v1 differ", cnode._value)
                cnode = cnode.get_next_node()

        cnode = chain2.get_head()
        while True:
            if (cnode == None):
                break
            if (cnode.id in map1):
                cnode = cnode.get_next_node()
            else:
                print("v2 differ", cnode._value)
                cnode = cnode.get_next_node()

    def compare_x(self):
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






