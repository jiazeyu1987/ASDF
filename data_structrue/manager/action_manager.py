from .. import *
class ActionUnit:
    def __init__(self,action,node_from,node_to):
        self.action = action
        self.node_from = node_from
        self.node_to = node_to

    def __str__(self):
        str1 = ""
        str1 = str1+self.action
        str1 = str1+" "+self.node_from.get_value()+" "+self.node_to.get_value()
        return str1

class ActionManager:
    def __init__(self):
        self.SIMPLE_LINK = "link"
        self.FIND = "find"


am = ActionManager()