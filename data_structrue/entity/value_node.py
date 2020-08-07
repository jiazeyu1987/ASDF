from data_structrue import NodeBase
from . import *
class ValueNode(NodeBase):
    VALUE_NOT_EXIST_MAX = -40
    VALUE_NOT_EXIST_MORE_MORE = -30
    VALUE_NOT_EXIST_MORE  = -20
    VALUE_NOT_EXIST = -10
    VALUE_NORMAL = 0
    VALUE_EXIST = 10
    VALUE_EXIST_MORE = 20
    VALUE_EXIST_MORE_MORE = 30
    VALUE_EXIST_MAX = 40
    def __init__(self,value):
        super().__init__(value)
        self.type = NodeBase.TYPE_VALUE

    def compare(self,node1,entity1,entity2):
        from . import EntityNode
        if(self.get_value()!=node1.get_value()):
            return [CompareValue(EntityNode.COMPARE_UNLIKE,self,node1,entity1,entity2)]

