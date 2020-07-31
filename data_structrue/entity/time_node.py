from data_structrue import NodeBase
from . import *
class TimeNode(NodeBase):
    def __init__(self):
        super().__init__("")
        self.type = NodeBase.TYPE_TIME

    def compare(self,node1):
        return []