'''
要求
1.拥有至少2级缓存区
    1.1 快速缓存区，也就是比对区，只存储2个chain
    1.2 慢速缓存区，快速缓存区的内容会不停移动到慢速缓存区
    目的：快读缓存区可以进行当前的相近的chain的对比，慢速缓存区可以进行大量的chain的对比
    使用：从慢速缓存区中发现相似点，寻找出相似点对应的chain，移动到快速缓存区进行对比
         直接快速缓存区发现对比

2.chain的对比
    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 node5 edge_type1 node6 edge_type2 node7
                           edge_type1 node8

    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 node15 edge_type1 node6 edge_type2 node7
                            edge_type1 node8

    当只有一个点不同的时候，将这个点替换成一个替代点，替代为
    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 nodeX edge_type1 node6 edge_type2 node7
                           edge_type1 node8

    node5 edge_type1001 nodeX
    node15 edge_type1001 nodeX



    假如不同的是两个替代点
    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 nodeX edge_type1 node6 edge_type2 node7
                           edge_type1 node8
    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 nodeY edge_type1 node6 edge_type2 node7
                           edge_type1 node8
    那么得出
    node1 edge_type1 node2
          edge_type1 node3
          edge_type2 node4
          edge_type1 nodeZ edge_type1 node6 edge_type2 node7
                           edge_type1 node8
    node5 edge_type1001 nodeX
    node15 edge_type1001 nodeX
    node25 edge_type1001 nodeY
    node35 edge_type1001 nodeY

    node5 edge_type1001 nodeZ
    node15 edge_type1001 nodeZ
    node25 edge_type1001 nodeZ
    node35 edge_type1001 nodeZ

3 chain 在进来之前要经过初加工
    每个节点将其附属的最大边值的点附带进来

4 两条chain进行对比之后有
    4.1 只有唯一一个节点不同，合并产生一个模型，模型由里面的节点产生对应线进行关联
    4.2 多个节点边点不同，放入永久区

5 edge类型
    连接模型的edge
    连接替代点的edge


'''
from . import *
from .. import *
class ImageManager:
    def __init__(self):
        self.cached_entity_node = None
        self.cached_chain_head = None
        self.str_tree = StupidTree()
        self.model_node_tree = StupidTree()
        self.cached_strlist = None


    def on_raw_data(self,strlist,in_entity_node):
        print(strlist)
        if(self.cached_strlist==None):
            self.cached_strlist = strlist
            self.cached_entity_node = in_entity_node
            return

        #首先查看是否可以读懂句子里的每个词语
        builded_model = self.get_build_model(strlist)
        cached_builded_model = self.get_build_model(self.cached_strlist)

        #如果可以读懂句子里的每个词语
        if(len(builded_model)>0):
            print("understand word:"+strlist.__str__())
            #查看是否可以将这些词语组合成自己可以理解的模型
            r,exist_model = self.model_node_tree.get_model(builded_model,EdgeBase.TYPE_NODE_TO_MODEL)
            if(r):
                print("understance model")
                #replace_node0_models 是完全理解的模型
                replace_node0_models = self.find_replace_node_only_n(exist_model, 0,builded_model)
                # replace_node1_models 是可以简单类推的模型
                replace_node1_models = self.find_replace_node_only_n(exist_model, 1,builded_model)

                if(len(replace_node0_models)>0):
                    print("know well")
                    replace_model = replace_node0_models[0]
                    self.cached_strlist = strlist
                    self.cached_entity_node = in_entity_node
                    return
                if(len(replace_node1_models)>0):
                    print("like other model")
                    replace_model = replace_node1_models[0]
                    replace_strlist = ""
                    replace_node1,replace_node2 = self.get_replace_node(builded_model,replace_model)

                    replace_entity_node = self.model_node_tree.get_extra_node(replace_model,EdgeBase.TYPE_NODE_TO_MODEL)
                    m1 = replace_entity_node.copy_model([EdgeBase.TYPE_NORMAL])
                    self.replace2(m1,replace_node1,replace_node2)
                    req = self.equal_model(m1,in_entity_node)
                    # for dd in replace_model:
                    #     print(dd)
                    # print(replace_entity_node)
                    # print(m1)
                    # print(self.cached_entity_node)
                    # print(in_entity_node)
                    print(req)
                    #self.model_node_tree.say()
                    if(req):
                        replace_node_parent = self.model_node_tree.get_node_by_id(replace_node2)
                        replace_node_parent.link(replace_node1.copy(),EdgeBase.TYPE_CONTAIN)
                        replace_node_parent.print_base([EdgeBase.TYPE_CONTAIN])
                        self.cached_strlist = strlist
                        self.cached_entity_node = in_entity_node
                        return


            self.model_node_tree.add_models(builded_model,in_entity_node,EdgeBase.TYPE_NODE_TO_MODEL)
            if(len(cached_builded_model)>0):
                cached_node = self.cached_entity_node.copy_model([EdgeBase.TYPE_NORMAL])
                in_node_copy = in_entity_node.copy_model([EdgeBase.TYPE_NORMAL])
                self.compare_node_model(cached_builded_model,builded_model,cached_node,in_node_copy)
                self.cached_strlist = strlist
                self.cached_entity_node = in_entity_node
                return
        else:
            print("don't know any thing")
            self.compare_strlist_model(strlist,in_entity_node)
            self.cached_strlist = strlist
            self.cached_entity_node = in_entity_node

    def equal_model(self,m1,in_entity_mode):
        if(m1.get_value()!=in_entity_mode.get_value()):
            if(m1.contain(in_entity_mode)!=None):
                return True
            if(in_entity_mode.contain(m1)!=None):
                return True
            return False
        for edge in m1.edge_list:
            node_to = edge.node_to
            has_flag = False
            for edge2 in in_entity_mode.edge_list:
                if(self.equal_model(node_to,edge2.node_to)==True):
                    has_flag = True
                    break
            if(has_flag==False):
                return False
        return True

    def replace2(self,model,rnode1,rnode2):
        value1 = model.get_value()
        rnodevalue = rnode2.get_value()
        if(rnodevalue==value1):
            model.replace_node(rnode1.get_value())
            return
        for edge in model.edge_list:
            node_to = edge.node_to
            self.replace2(node_to,rnode1,rnode2)

    def get_replace_node(self,builded_model,replace_model):
        for node1 in builded_model:
            has_flag = False
            for node2 in replace_model:
                if (node1.get_value() == node2.get_value()):
                    has_flag = True
                    break
            if (has_flag == False):
                for node2 in replace_model:
                    if (node2.get_value()[0] == "瓛"):
                        return node1,node2
        return None,None

    def find_replace_node_only_n(self,modelss,n,builded_model):
        arr = []
        for model in modelss:
            index=0

            for i in range(len(model)):
                node1 = model[i]
                node2 = builded_model[i]
                if(node1.get_value()==node2.get_value()):
                    continue
                if(node1.get_value()[0]=="瓛"):
                    if(node1.contain(node2)!=None):
                        continue
                    else:
                        index+=1
            if (index == n):
                arr.append(model)
        return arr

    def compare_node_model(self,cached_node_list,in_node_list,cached_entity_node,in_entity_node):
        node_map = {}
        self.mark_node_list(cached_node_list, node_map)
        self.mark_node_list(in_node_list, node_map)
        #print(node_map)
        node_arr = []
        #['房', '子', '非', '常', '美']
        for key in node_map:
            if (node_map[key] == 1):
                node_arr.append(key)
        if (len(node_arr) == 2):
            replace_node = NodeBase.create_node(NodeBase.VALUE_REPLACE+(NodeBase.NODE_BASE_ID+1).__str__())
            chain1 = self.create_replace_node_by_1(cached_node_list,node_arr,replace_node)
            chain2 = self.create_replace_node_by_1(in_node_list, node_arr, replace_node)
            self.create_replace_node_by_2(in_entity_node,node_arr,replace_node)
            self.create_replace_node_by_2(cached_entity_node, node_arr, replace_node)
            self.model_node_tree.add_models(chain1.get_node_list(), cached_entity_node, EdgeBase.TYPE_NODE_TO_MODEL)
            self.model_node_tree.add_models(chain2.get_node_list(), in_entity_node, EdgeBase.TYPE_NODE_TO_MODEL)
            # print(chain1)
            # print(chain2)
            # print(in_entity_node)
            # print(cached_entity_node)
            # replace_node.print([EdgeBase.TYPE_CONTAIN])

    def create_replace_node_by_2(self,in_entity_node,node_arr,replace_node):
        if(in_entity_node.get_value() in node_arr):
            in_entity_node.replace_node(replace_node.get_value())
        for edge in in_entity_node.edge_list:
            self.create_replace_node_by_2(edge.node_to,node_arr,replace_node)

    def create_replace_node_by_1(self,nodelist,node_arr,replace_node):
        chain = SimpleNodeChain()
        head = chain.get_head()
        for node in nodelist:
            if(node.get_value() in node_arr):
                replace_node.link(node.copy(),EdgeBase.TYPE_CONTAIN)
                head.link(replace_node,EdgeBase.TYPE_NORMAL)
                head = replace_node
            else:
                if(head==None):
                    head = node.copy()
                else:
                    node_copy = node.copy()
                    head.link(node_copy,EdgeBase.TYPE_NORMAL)
                    head = node_copy
        return chain


    def mark_node_list(self,nodelist,node_map):
        for node in nodelist:
            value = node.get_value()
            if(value in node_map):
                node_map[value]+=1
            else:
                node_map[value]=1

    def compare_strlist_model(self,strlist,in_node):
        str_map = {}
        self.map_strlist(self.cached_strlist,str_map)
        self.map_strlist(strlist, str_map)
        node_map = {}
        self.map_node(self.cached_entity_node, node_map)
        self.map_node(in_node, node_map)
        #print(node_map)
        str_arr = []
        for key in str_map:
            if(str_map[key]==1):
                str_arr.append(key)
        node_arr = []
        for key in node_map:
            if(node_map[key]==1):
                node_arr.append(key)
        if(len(node_arr)==2):
            str_list_sub = self.locate_strlist(strlist,str_arr)
            node_sub = self.locate_node(in_node,node_arr)
            self.bind_strlist_to_node(str_list_sub,node_sub)

            str_list_sub = self.locate_strlist(self.cached_strlist, str_arr)
            node_sub = self.locate_node(self.cached_entity_node, node_arr)
            self.bind_strlist_to_node(str_list_sub, node_sub)


    def bind_strlist_to_node(self,strlist,node):
        self.str_tree.add_value(strlist,node,EdgeBase.TYPE_WORD_TO_NODE)
        #self.str_tree.say()

    def locate_node(self,in_node,node_arr):
        node = None
        val1 = in_node.get_value()
        for node_value in node_arr:
            if(val1==node_value):
                return in_node.copy()
        for edge in in_node.edge_list:
            node_to = edge.node_to
            node1 = self.locate_node(node_to,node_arr)
            if(node1!=None):
                return node1.copy()
        return None

    def locate_strlist(self,strlist,str_arr):
        arr = []
        for char in strlist:
            for char2 in str_arr:
                if(char==char2):
                    arr.append(char)
        return arr


    def map_strlist(self,strlist1,map1):
        for char1 in strlist1:
            if(char1 in map1):
                map1[char1]+=1
            else:
                map1[char1]=1

    def get_build_model(self,strlist):
        nodes_arr = []
        cal = self._get_build_model(strlist,0,nodes_arr)
        nodes_arr.reverse()
        return nodes_arr

    def _get_build_model(self,strlist,index,nodes_arr):
        if(index==len(strlist)):
            return True

        nodelist,lenlist = self.str_tree.get_linked_node_by_strlist(strlist[index:],EdgeBase.TYPE_WORD_TO_NODE)

        if(len(nodelist)==0):
            return False

        for i in range(len(nodelist)):
            node1 = nodelist[i]
            len1 = lenlist[i]
            r = self._get_build_model(strlist,index+len1,nodes_arr)
            if(r==True):
                nodes_arr.append(node1.copy())
                return True
        return False

    '''
        输入node
    '''
    def on_enter_node(self,chain_head,in_entity_node):
        self.link_1_to_2(chain_head,in_entity_node)
        #in_entity_node.print([EdgeBase.TYPE_NORMAL,EdgeBase.TYPE_LINK_TO_1Dimension])

        if(self.cached_entity_node==None):
            self.cached_entity_node = in_entity_node
            self.cached_chain_head = chain_head
        else:
            if(self.cached_entity_node!=None):
                #returnlist = self.get_all_returnvalue(self.cached_entity_node,in_entity_node)
                chain1, chain2 = self.compare_and_model(self.cached_chain_head, chain_head)
                node1,node2 = self.model_1(self.cached_entity_node,in_entity_node)

                #self.link_model_1_to_2(node1,chain1)
                print(node1)
                print(node2)
                print(chain1)
                print(chain2)

            self.cached_entity_node = in_entity_node
            self.cached_chain_head = chain_head



    def link_1_to_2(self,chain_head,entity_node):
        cnode = chain_head.get_head()
        while True:
            cnode = cnode.get_next_node()
            if(cnode == None):
                break
            self.link_chain_node_to_2(cnode,entity_node)


    def link_chain_node_to_2(self,cnode,entity_node):
        if(entity_node.get_value()==cnode.get_value()):
            cnode.link(entity_node,EdgeBase.TYPE_LINK_TO_2Dimension)
            entity_node.link(cnode, EdgeBase.TYPE_LINK_TO_1Dimension)
        for edge in entity_node.edge_list:
            if(edge.type!=EdgeBase.TYPE_NORMAL):
                continue
            node_to = edge.node_to
            self.link_chain_node_to_2(cnode,node_to)


    def compare_and_model(self,chain1,chain2):
        from .. import im, mt
        map1 = {}

        chain_map = {}
        self.simple_mark_chain_node(chain1, chain_map)
        self.simple_mark_chain_node(chain2, chain_map)
        self.ff(chain1,chain_map,map1)
        self.ff(chain2, chain_map, map1)

        new_replace_chain1 = self.replace_differ_node(chain1,map1)
        new_replace_chain2 = self.replace_differ_node(chain2, map1)
        return new_replace_chain1,new_replace_chain2

    def ff(self,chain1,chain_map,map1):
        cnode1 = chain1.get_head()
        while True:
            cnode1 = cnode1.get_next_node()
            if (cnode1 == None):
                break
            if (cnode1.get_value() in chain_map):
                if(chain_map[cnode1.get_value()]>1):
                    map1[cnode1.id]=1

    def simple_mark_chain_node(self,chain1,map1):
        cnode1 = chain1.get_head()
        while True:
            cnode1 = cnode1.get_next_node()
            if(cnode1==None):
                break
            if(cnode1.get_value() in map1):
                map1[cnode1.get_value()]+=1
            else:
                map1[cnode1.get_value()]=1

    def replace_differ_node(self, chain1, map1):
        cnode = chain1.get_head()
        cnode = cnode.get_next_node()
        new_chain1 = SimpleNodeChain()
        current_flag = 1
        replace_node = None
        while True:
            if (cnode == None):
                break
            #print(cnode._value)
            if (cnode.id in map1):
                if(replace_node!=None):
                    replace_node = None
                current_flag = 1
                #print("1111111111111")
                new_chain1.add_new_node_by_char(cnode.get_value())
                cnode = cnode.get_next_node()
            else:
                #print("22222222")
                if (current_flag == 1):
                    replace_node = ReplaceNode()
                    new_chain1.add_node(replace_node)
                    current_flag = 1
                replace_node.add_node_by_value(cnode)
                cnode = cnode.get_next_node()
        if (replace_node != None):
            replace_node = None
        return new_chain1

    def compare_simple_node_chain(self,chain1:SimpleNodeChain,chain2:SimpleNodeChain,map1):
        from .. import FastMap
        add_weight = 1
        map_compare = FastMap()

        edgelist = self.get_fast_impression(chain1,chain2,map_compare,add_weight)

        while True:
            max_len,node1,node2 = self.get_max_len(chain1,chain2,edgelist,add_weight,map1)
            if(max_len==0):
                break
            self.mark_chain(chain1,max_len,node1,map1)
            self.mark_chain(chain2, max_len, node2, map1)
        return chain1,chain2

    def mark_chain(self,chain1,len,node1,map1):
        cnode = chain1.get_head()
        index=-1
        while True:
            if(cnode==None):
                break
            if(cnode.id==node1.id):
                index=0
                cnode = cnode.get_next_node()
                continue
            if(index==-1):
                cnode = cnode.get_next_node()
                continue
            map1[cnode.id] = 1
            index+=1
            cnode = cnode.get_next_node()
            if(index==len-1):
                break

    def get_max_len(self,chain1:SimpleNodeChain,chain2:SimpleNodeChain,edgelist,add_weight,map1):
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
                if(simple_node.id in map1):
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
        if(max_chain_len!=0):
            map1[max_node1.id] = 1
            map1[max_node2.id] = 1
        return max_chain_len,max_node1,max_node2

    def get_fast_impression(self,chain1,chain2,map_compare,add_weight):
        from .. import FastChain
        fast_chain1 = FastChain(chain1, map_compare, add_weight)
        fast_chain2 = FastChain(chain2, map_compare, add_weight)
        return fast_chain2.edgelist

    def model_1(self,cached_node,in_node):
        map1 = {}
        self.map_node(cached_node,map1)
        self.map_node(in_node,map1)
        node1 = self.model_by_node_map(cached_node,map1)
        node2 = self.model_by_node_map(in_node, map1)
        return node1,node2

    def model_by_node_map(self,in_node,map1):

        value1 = in_node.get_value()

        if(value1 in map1):

            if(map1[value1]>1):
                node = NodeBase(value1)
            else:
                link1dmenNodes = in_node.get_node_by_edge_type(EdgeBase.TYPE_LINK_TO_1Dimension)
                if(len(link1dmenNodes)==0):
                    node = ReplaceNode()
                    node.add_node_by_value(node)
                else:
                    demen1Node = link1dmenNodes[0]
                    replace_nodes = demen1Node.get_node_by_edge_type(EdgeBase.TYPE_BELONG)
                    if(len(replace_nodes)>0):
                        node = replace_nodes[0].copy()
                        map1[node.get_value()]=1
                    else:
                        raise Exception("FFFFFFFFF")

            for edge in in_node.edge_list:
                if(edge.type==EdgeBase.TYPE_NORMAL):
                    node_to = edge.node_to
                    new_node = self.model_by_node_map(node_to,map1)
                    node.link(new_node,EdgeBase.TYPE_NORMAL)
            return node
        else:
            raise Exception(value1.__str__())

    def map_node(self,in_node,map1):
        if(in_node.get_value() in map1):
            map1[in_node.get_value()]+=1
        else:
            map1[in_node.get_value()]=1

        for edge in in_node.edge_list:
            if(edge.type == EdgeBase.TYPE_NORMAL):
                self.map_node(edge.node_to,map1)

    def model_2(self,cached_node,in_node):
        node_more_list, node_equal_list, node_less_list = self.get_compare_node_list_simple(cached_node, in_node,
                                                                                     [EdgeBase.TYPE_NORMAL])
        if(len(node_equal_list)==0 and cached_node.get_value()!=in_node.get_value()):
            print(1)
            return None
        elif(len(node_equal_list)==0):
            print(2)
            return NodeBase(cached_node.get_value())
        elif(cached_node.get_value()!=in_node.get_value()):
            print(3)
            replace_node = ReplaceNode()
            for i in range(0,len(node_equal_list),2):
                edge1 = node_equal_list[i]
                edge2 = node_equal_list[i+1]
                node_to1 = edge1.node_to
                node_to2 = edge2.node_to
                replace_node.link(self.model_1(node_to1,node_to2),EdgeBase.TYPE_NORMAL)
            return replace_node
        else:
            print(4)
            new_node = NodeBase(cached_node.get_value())
            for i in range(0,len(node_equal_list),2):
                edge1 = node_equal_list[i]
                edge2 = node_equal_list[i+1]
                node_to1 = edge1.node_to
                node_to2 = edge2.node_to
                new_node.link(self.model_1(node_to1,node_to2),EdgeBase.TYPE_NORMAL)
            return new_node




    def map_edge(self,in_node,map1):
        for edge in in_node.edge_list:
            node_to = edge.node_to
            value1 = node_to.get_value()
            if(value1 in map1):
                map1[value1]+=1
            else:
                map1[vlaue1]=1


    def get_all_returnvalue(self,cached_node,in_node):
            node_more_list, node_equal_list, node_less_list = self.get_compare_node_list(cached_node,in_node,[EdgeBase.TYPE_NORMAL])
            map_equal = {}
            map_differ = {}
            for vl in node_equal_list:
                print(vl)
            self.mark_equal_edge(in_node,node_equal_list,map_equal,map_differ)
            tmplist = []
            returnlist = []
            self.get_actionlist(in_node,map_differ,tmplist,returnlist)
            for edge in returnlist:
                for e in edge:
                    print(e)
            return returnlist


    def get_actionlist(self,entity_node,map_differ,tmplist,returnlist):
        for edge in entity_node.edge_list:
            if(edge.id in map_differ):
                returnlist.append(tmplist+[ActionUnit(am.SIMPLE_LINK,edge.node_from,edge.node_to)])
            else:
                node_to = edge.node_to
                self.get_actionlist(node_to,map_differ,tmplist+[ActionUnit(am.FIND,edge.node_from,edge.node_to)],returnlist)



    def mark_equal_edge(self,in_entity_node,node_equal_list,map_equal,map_differ):
        for edge in in_entity_node.edge_list:
            has_flag = False
            for equal_edge in node_equal_list:
                if(edge.value_equal(equal_edge)):
                    map_equal[edge.id]=1
                    has_flag = True
                    break
            if(has_flag==False):
                map_differ[edge.id]=1
            self.mark_equal_edge(edge.node_to,node_equal_list,map_equal,map_differ)





    def handler_differ(self,cached_node,in_node,differ):
        if(differ==0):
            return
        if(differ>2):
            return
        if(differ==1):
            #todo
            return
        if(differ==2):
            self.handler_2_differ(cached_node,in_node)

    def create_replace_node(self,node1,node2,node1_parent,node2_parent):
        node_replace = NodeBase(NodeBase.VALUE_REPLACE)
        node_replace.type = NodeBase.TYPE_REPLACE

        node_replace.edge_list = node1.edge_list+node2.edge_list
        node1.edge_list = []
        node2.edge_list = []
        for edge in node_replace.edge_list:
            edge.node_from = node_replace



        if(node1_parent!=None):
            for edge in node1_parent.edge_list:
                if(edge.node_to.get_value()==node1.get_value()):
                    edge.node_to = node_replace
            for edgekey in node1_parent.follow_edge_map:
                edge = node1_parent.follow_edge_map[edgekey]
                if (edge.node_to.get_value() == node1.get_value()):
                    edge.node_to = node_replace

        if (node2_parent != None):
            for edge in node2_parent.edge_list:
                if (edge.node_to.get_value() == node2.get_value()):
                    edge.node_to = node_replace
            for edgekey in node2_parent.follow_edge_map:
                edge = node2_parent.follow_edge_map[edgekey]
                if (edge.node_to.get_value() == node2.get_value()):
                    edge.node_to = node_replace

        node1.link(node_replace,EdgeBase.TYPE_BELONG)
        node2.link(node_replace, EdgeBase.TYPE_BELONG)
        node_replace.link(node1, EdgeBase.TYPE_CONTAIN)
        node_replace.link(node2, EdgeBase.TYPE_CONTAIN)
        print(node_replace)



    def handler_2_differ(self, cached_entity_node, in_node):
        if (cached_entity_node.get_value() != in_node.get_value()):
            self.create_replace_node(cached_entity_node,in_node,None,None)


    def get_compare_node_list_simple(self,cached_entity_node,in_node,whitelist,in_number = 0):
        more_list = []
        equal_list = []
        less_list = []
        for edge in cached_entity_node.edge_list:
            if(edge.type in whitelist == False):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in in_node.edge_list:
                if (in_edge.type in whitelist == False):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value()):
                    equal_list.append(edge)
                    equal_list.append(in_edge)
                    has_flag = True
                    break
            if (has_flag == False):
                more_list.append(edge)


        for edge in in_node.edge_list:
            if (edge.type in whitelist == False):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in cached_entity_node.edge_list:
                if (in_edge.type in whitelist == False):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value()):
                    has_flag = True
                    break
            if (has_flag == False):
                less_list.append(edge)



        return more_list,equal_list,less_list


    def get_compare_node_list(self,cached_entity_node,in_node,whitelist,in_number = 0):
        more_list = []
        equal_list = []
        less_list = []
        for edge in cached_entity_node.edge_list:
            if(edge.type in whitelist == False):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in in_node.edge_list:
                if (in_edge.type in whitelist == False):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value() and edge.node_from.get_value()==in_edge.node_to.get_value()):
                    equal_list.append(edge)
                    equal_list.append(in_edge)
                    more_list_sub,equal_list_sub,less_list_sub = self.get_compare_node_list(node_to,in_node_to,whitelist)
                    more_list = more_list+more_list_sub
                    equal_list = equal_list+equal_list_sub
                    less_list = less_list+less_list_sub
                    has_flag = True
                    break
            if (has_flag == False):
                more_list.append(edge)


        for edge in in_node.edge_list:
            if (edge.type in whitelist == False):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in cached_entity_node.edge_list:
                if (in_edge.type in whitelist == False):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value()):
                    has_flag = True
                    break
            if (has_flag == False):
                less_list.append(edge)



        return more_list,equal_list,less_list

im = ImageManager()