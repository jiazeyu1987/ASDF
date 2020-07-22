from .. import EdgeBase
class MemoryEdge(EdgeBase):
    EDGE_CONTAIN = 1
    EDGE_NORMAL = 2
    EDGE_RELATION = 3
    EDGE_ID = 1
    def __init__(self,node_from,node_to,type = EDGE_NORMAL,strong=1):
        super().__init__(node_from,node_to,strong)
        self.type = type
        self.id = MemoryEdge.EDGE_ID
        MemoryEdge.EDGE_ID+=1

    def get_type(self):
        if(self.type==MemoryEdge.EDGE_NORMAL):
            return "normal"
        elif (self.type==MemoryEdge.EDGE_CONTAIN):
            return "contain"
        elif (self.type==MemoryEdge.EDGE_RELATION):
            return "relation"
        else:
            raise Exception("JLkfjlasdkjflsakdjf")