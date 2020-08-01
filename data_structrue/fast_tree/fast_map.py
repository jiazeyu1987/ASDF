from .. import NodeBase
import  globalconfig as g
class FastMap:
    def __init__(self):
        self.map = {}
        self.edgelist = {}

    def get_map(self):
        return self.map


    def __str__(self):
        str1 = ""
        for key in self.map:
            str1 = str1+"key:"+key+" - NodeWeight:"+self.map[key].strong.__str__()+"\n"
        return str1