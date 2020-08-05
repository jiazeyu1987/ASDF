class EdgeBase:
    TYPE_NORMAL = "normal"
    TYPE_INFO = "info"
    TYPE_REPLACE = "replace"
    TYPE_LINK_OUTER = 3
    TYPE_LINK_ACTION = 4
    TYPE_BELONG = "belong"
    TYPE_CONTAIN = "contain"
    TYPE_LINK_TO_2Dimension = "link_to_2"
    TYPE_LINK_TO_1Dimension = "link_to_1"
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


    def value_equal(self,edge):
        if(self.node_from.get_value()==edge.node_from.get_value() and
        self.node_to.get_value()==edge.node_to.get_value()):
            return True
        return False

    def __str__(self):
        str1 = "edge info weight:"+self.strong.__str__()
        str1 = str1+"   "+self.node_from.get_value().__str__()
        str1 = str1+" to "+self.node_to. get_value().__str__()
        return str1