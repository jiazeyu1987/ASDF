from .. import *
import globalconfig as g
class FastEdge(EdgeBase):
    def __init__(self,node_from,node_to,strong=1):
        super().__init__(node_from,node_to,strong)


    def add_weight(self):
        self.strong+=g.add_weight_number

    def lose_weight(self):
        self.strong-=g.lose_weight_number

    def is_strong_enough(self):
        return self.strong>1+g.add_weight_number