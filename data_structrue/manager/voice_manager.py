from .. import *
class VoiceManager:
    def __init__(self):
        self.main_map = {}
        self.key_map = {}
        self.stupid_tree = StupidTree()

    def link(self, snc, info_node):
        key_arr = snc.get_key()
        self.stupid_tree.add_value(key_arr,info_node,EdgeBase.TYPE_LINK_OUTER)
        self.analyse(key_arr,info_node)



    def analyse(self,key_arr,info_node):
        if(len(key_arr)==1):
            key = key_arr[0]
            #find first entity node
            info_head = info_node.get_head()
            if(info_head==None):
                return

            #find word related
            node1,depth1 = self.stupid_tree.get_nearest(key)
            if(node1==None):
                return

            #handle entity for tmp
            if(info_head.type==NodeBase.TYPE_ENTITY):
                node1.add_action(NodeBase.ACTION_CREATE,info_head,info_head)
            else:
                raise Exception("to do later")
            return

        info_node2 = InfoNode()
        pass_arr = []
        for key in key_arr:
            #find nearest word related
            node1,depth1 = self.stupid_tree.get_nearest(key)
            if(node1==None):
                return
            action_edge = node1.get_one1_action()
            if(action_edge==None):
                pass_arr.append(key)
            else:
                self.play_action(info_node2,action_edge)


        v1arr = info_node.compare_info_node(info_node2)
        if(len(v1arr)==0):
            return

        self.guess_pass(pass_arr,v1arr)


    def guess_pass(self,pass_arr,v1arr):
        for i in range(len(pass_arr)):
            pass_node = pass_arr[i]
            self.guess_pass_node(pass_node,v1arr)

    def guess_pass_node(self,pass_node,v1arr):
        node1, depth1 = self.stupid_tree.get_nearest(pass_node)
        if (node1 == None):
            return
        for compare_value in v1arr:
            if(compare_value.type == NodeBase.COMPARE_LACK):
                node1.add_action(NodeBase.ACTION_CREATE,compare_value.node1,compare_value.node1_parent)



    def play_action(self,info_node,action_edge):
        action_node = action_edge.node_to
        if(action_node.get_value()==NodeBase.ACTION_CREATE):
            node1 = action_node.get_next_node_by_edge(EdgeBase.TYPE_LINK_ACTION)
            node_parent = node1.get_next_node_by_edge(EdgeBase.TYPE_LINK_ACTION)
            info_node.create_node(node1,node_parent)


    # def link2(self,snc,entity_node):
    #     key_arr = snc.get_key()
    #     whole_key = key_arr.__str__()
    #     if(whole_key in self.main_map):
    #         old_node = self.main_map[whole_key]
    #         child = old_node.get_voice_child(entity_node,EdgeBase.TYPE_NORMAL)
    #         if(child!=None):
    #             old_node.add_voice_child_weight(child)
    #         else:
    #             old_node.add_voice_child(entity_node,EdgeBase.TYPE_NORMAL)
    #     else:
    #         self.main_map[whole_key] = NodeBase("")
    #         self.main_map[whole_key].add_voice_child(entity_node,EdgeBase.TYPE_NORMAL)
    #
    #     for key in key_arr:
    #         if(key in self.key_map):
    #             vals = self.key_map[key]
    #             if(whole_key in vals):
    #                 pass
    #             else:
    #                 vals[whole_key] = 1
    #         else:
    #             self.key_map[key] = {}
    #             self.key_map[key][whole_key] = 1
vm = VoiceManager()