from .. import *
import globalconfig as g
import math
class StupidEdge(EdgeBase):
    def __init__(self,node_from,node_to,strong=0):
        super().__init__(node_from,node_to,strong)
        self.add_index_orgin = 1
        self.add_index = self.add_index_orgin
        self.minus_index = 1


    def add_stupid_weight(self):
        self.add_index+=1
        self.strong += (int)((math.log(self.add_index,10)-math.log(self.add_index-1,10))*100)


    def minus_stupid_weight(self):
        self.minus_index+=1
        self.strong = (int)(self.strong/self.minus_index)


    def reset(self):
        self.add_index = self.add_index_orgin

