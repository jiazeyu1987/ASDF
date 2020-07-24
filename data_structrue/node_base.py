class NodeBase:
    def __init__(self,value,strong=0):
        self.value = value
        self.strong = 0

    def add_weight(self,weight):
        self.strong+=weight

    def lose_weight(self,weight):
        self.strong-=weight
        