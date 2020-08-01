from data_structrue import NodeBase
from . import *
class NumberNode(NodeBase):
    def __init__(self):
        super().__init__("")
        self.type = NodeBase.TYPE_NUMBER

    def compare(self,node1):
        return []