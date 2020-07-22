class EdgeBase:
    def __init__(self,node_from,node_to,strong=1):
        self.node_from = node_from
        self.node_to = node_to
        self.strong = strong

    def add_weight(self):
        self.strong+=1