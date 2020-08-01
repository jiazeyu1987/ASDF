from data_structrue import NodeBase
from . import *
class AddressNode(NodeBase):
    def __init__(self):
        super().__init__("")
        self.type = NodeBase.TYPE_ADDRESS


    def compare(self,node1):
        return []