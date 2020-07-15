from .. import NodeBase
class SimpleNodeChainNode(NodeBase):
    def __init__(self,value):
        super().__init__(value)
        self.follow_edge = None



