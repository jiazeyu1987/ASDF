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

    '''
        输入node
    '''
    def on_enter_node(self,in_entity_node):
        if(self.cached_entity_node==None):
            self.cached_entity_node = in_entity_node
        else:
            differ = self.compare_node(self.cached_entity_node,in_entity_node)
            self.handler_differ(self.cached_entity_node,in_entity_node,differ)
            self.cached_entity_node = in_entity_node


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

        for key1 in node1.follow_edge_map:
            node_replace.follow_edge_map[key1] = node1.follow_edge_map[key1]
        for key1 in node2.follow_edge_map:
            node_replace.follow_edge_map[key1] = node2.follow_edge_map[key1]
        for key1 in node_replace.follow_edge_map:
            node_replace.follow_edge_map[key1].node_from = node_replace
        node1.follow_edge_map = {}
        node2.follow_edge_map = {}

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

    '''
        找出只有一个点不同的情况
    '''
    def compare_node(self,cached_entity_node,in_node,in_number = 0):
        differ = 0
        if(cached_entity_node.get_value()!=in_node.get_value()):
            differ+=2
        for edge in cached_entity_node.edge_list:
            if(edge.type!=EdgeBase.TYPE_NORMAL):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in in_node.edge_list:
                if (in_edge.type != EdgeBase.TYPE_NORMAL):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value()):
                    differ = differ + self.compare_node(node_to, in_node_to)
                    has_flag = True
                    break
            if (has_flag == False):
                differ += 1

        for edge in in_node.edge_list:
            if (edge.type != EdgeBase.TYPE_NORMAL):
                continue
            node_to = edge.node_to
            has_flag = False
            for in_edge in cached_entity_node.edge_list:
                if (in_edge.type != EdgeBase.TYPE_NORMAL):
                    continue
                in_node_to = in_edge.node_to
                if (node_to.get_value() == in_node_to.get_value()):
                    has_flag = True
                    break
            if (has_flag == False):
                differ += 1

        for key in in_node.follow_edge_map:
            has_flag = False
            edge1 = in_node.follow_edge_map[key]
            if(edge1.type!=EdgeBase.TYPE_NORMAL):
                continue
            for key2 in cached_entity_node.follow_edge_map:
                edge2 = cached_entity_node.follow_edge_map[key2]
                if (edge2.type != EdgeBase.TYPE_NORMAL):
                    continue
                if (edge1.node_to.get_value() == edge2.node_to.get_value()):
                    differ = differ + self.compare_node(in_node.follow_edge_map[key].node_to,
                                                        cached_entity_node.follow_edge_map[key2].node_to)
                    has_flag = True
            if (has_flag == False):
                differ += 1

        for key in cached_entity_node.follow_edge_map:
            edge1 = cached_entity_node.follow_edge_map[key]
            if(edge1.type!=EdgeBase.TYPE_NORMAL):
                continue
            has_flag = False
            for key2 in in_node.follow_edge_map:
                edge2 = in_node.follow_edge_map[key2]
                if (edge2.type != EdgeBase.TYPE_NORMAL):
                    continue
                if (edge1.node_to.get_value() == edge2.node_to.get_value()):
                    has_flag = True
                    break
            if (has_flag == False):
                differ += 1

        return differ

im = ImageManager()