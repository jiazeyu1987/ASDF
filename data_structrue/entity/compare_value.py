class CompareValue:
    def __init__(self,type,node1,node2,related_entity_node_1,related_entity_node_2):
        self.type = type
        self.node1 = node1
        self.node1_parent = related_entity_node_1
        self.node2 = node2
        self.node2_parent = related_entity_node_2

    def __str__(self):
        from .. import NodeBase
        str1 = ""
        if(self.type==NodeBase.COMPARE_MORE):
            str1 = "compare more:"
            str1 = str1+" "+self.node2.type.__str__()+" "+self.node2.get_value()+" "+self.node2_parent.get_value()
        if(self.type==NodeBase.COMPARE_LACK):
            str1 = "compare lack:"
            str1 = str1+" "+self.node1.type.__str__()+" "+self.node1.get_value()+" "+self.node1_parent.get_value()
        if(self.type==NodeBase.COMPARE_UNLIKE):
            str1 = "compare unlack:"
            str1 = str1+self.node1.get_value()+"-"+self.node2.get_value()
        return str1