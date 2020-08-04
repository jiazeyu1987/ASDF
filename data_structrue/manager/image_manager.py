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
    '''
        输入node
    '''
    def on_enter_node(self,chain_head,in_entity_node):
        if(self.cached_entity_node==None):
            self.cached_entity_node = in_entity_node
            self.cached_chain_head = chain_head
        else:
            returnlist = self.get_all_returnvalue(self.cached_chain_head,chain_head)
            for edge in returnlist:
                for e in edge:
                    print(e)
            self.cached_entity_node = in_entity_node
            self.cached_chain_head = chain_head

    def get_all_returnvalue(self,cached_node,in_node):
            node_more_list, node_equal_list, node_less_list = self.get_compare_node_list(cached_node,in_node,[EdgeBase.TYPE_NORMAL])
            map_equal = {}
            map_differ = {}
            self.mark_equal_edge(in_node,node_equal_list,map_equal,map_differ)

            tmplist = []
            returnlist = []
            self.get_actionlist(in_node,map_differ,tmplist,returnlist)
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
                if (node_to.get_value() == in_node_to.get_value()):
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