class EdgeBase:
    TYPE_NORMAL = 0
    TYPE_INFO = 1
    TYPE_REPLACE = 2
    TYPE_LINK_OUTER = 3
    TYPE_LINK_ACTION = 4
    TYPE_BELONG = "belong"
    TYPE_CONTAIN = "contain"
    EDGE_ID = 1
    def __init__(self,node_from,node_to,strong=0):
        self.node_from = node_from
        self.node_to = node_to
        self.strong = strong
        self.type = EdgeBase.TYPE_NORMAL
        self.id = EdgeBase.EDGE_ID
        EdgeBase.EDGE_ID+=1

    def add_weight(self,weight):
        self.strong+=weight

    def lose_weight(self,weight):
        self.strong-=weight


    def __str__(self):
        str1 = "edge info weight:"+self.strong.__str__()
        str1 = str1+"   "+self.node_from.value.__str__()
        str1 = str1+" to "+self.node_to.value.__str__()
        return str1