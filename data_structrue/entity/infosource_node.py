from data_structrue import NodeBase
class InfoSourceNode(NodeBase):
    def __init__(self):
        super().__init__("")
        self.type = NodeBase.TYPE_INFO_SOURCE