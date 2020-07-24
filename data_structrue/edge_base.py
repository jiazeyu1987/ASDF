class EdgeBase:
    def __init__(self,node_from,node_to,strong=0):
        self.node_from = node_from
        self.node_to = node_to
        self.strong = strong

    def add_weight(self,weight):
        self.strong+=weight

    def lose_weight(self,weight):
        self.strong-=weight