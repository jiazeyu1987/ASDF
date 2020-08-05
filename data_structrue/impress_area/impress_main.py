from .. import *
from .impress_main_page import ImpressMainPage
class ImpressMain(ImpressMainPage):
    def __init__(self):
        ImpressMainPage.__init__(self)
        self.last_compare_index = 0
        self.result_arr = []
        self.last_chain_index = 0

    def test(self):
        simple_node_chain = SimpleNodeChain()
        simple_node_chain.add_nodes_by_charlist("天周日天气不错")
        self.add_simple_node_chain(simple_node_chain)

        simple_node_chain = SimpleNodeChain()
        simple_node_chain.add_nodes_by_charlist("图星期天天气不错")
        self.add_simple_node_chain(simple_node_chain)

        self.compare()

    def compare_unit(self,source_row,compare_row):
        arr = []
        for i in range(self.last_compare_index,len(source_row)):
            unit = source_row[i]
            if (self.is_empty_value(unit)):
                continue
            Flag = False
            for j in range(len(compare_row)):
                if(compare_row[j]==unit):
                    arr.append([i,j])
                    Flag = True
            if(Flag):
                self.last_compare_index=i+1
                break
        if(len(arr)==0):
            return False
        else:
            self.result_arr.append(arr)



    def chain_neighbor_unit(self,source_row,compare_row):
        if(self.last_chain_index+1>len(self.result_arr)-1):
            return False
        unit_head_list = self.result_arr[self.last_chain_index]
        unit_tail_list = self.result_arr[self.last_chain_index+1]
        for unit_head in unit_head_list:
            for unit_tail in unit_tail_list:
                if(unit_tail[1]-unit_head[1]==1 and unit_tail[0]-unit_head[0]==1):
                    source_row[unit_head[0]][2]=1
                    source_row[unit_tail[0]][2] = 1
                    compare_row[unit_head[1]][2] = 1
                    compare_row[unit_tail[1]][2] = 1
        self.last_chain_index += 1
        return True


    def compare(self):
        self.last_chain_index = 0
        self.last_compare_index = 0
        tmp_arr = self.get_compare_row()
        if(len(tmp_arr)<2):
            return
        source_row,compare_row = tmp_arr[0],tmp_arr[1]

        while True:
            r = self.compare_unit(source_row,compare_row)
            if(r==False):
                break

        if(len(self.result_arr)<2):
            return

        while True:
            r = self.chain_neighbor_unit(source_row,compare_row)
            if(r==False):
                break
        g.p("im", "source_row:" + source_row.__str__())
        g.p("im", "compare_row:" + compare_row.__str__())

        self.mark(source_row)
        self.mark(compare_row)

        # source_head = self.mark_head(source_row)
        # compare_head = self.mark_head(compare_row)
        # source_tail = self.mark_tail(source_row)
        # compare_tail = self.mark_tail(compare_row)
        # body = self.mark_body(source_row)
        # g.p("im", "head:" + source_head.__str__())
        # g.p("im", "body:" + body.__str__())
        # g.p("im", "tail:" + source_tail.__str__())
        # self.save_to_brain([source_head,compare_head],body,[source_tail,compare_tail])

    def mark(self,data_row):
        arr = []
        flag = -1
        str1 = ""
        for char in data_row:
            if(flag==-1):
                flag = char[2]
                str1 = str1+char[0]
            else:
                if(flag!=char[2]):
                    arr.append(str1)
                    str1 = char[0]
                    flag = char[2]
                else:
                    str1 = str1+char[0]
        if(str1!=""):
            arr.append(str1)
        print(arr)

    def save_to_brain(self,source_list,body,tail_list):
        head_node = MemoryNode()
        for i in range(len(source_list)):
            source_unit = source_list[i]
            str1 = ""
            for uunit in source_unit:
                str1 = str1+uunit[0]
            if (str1 == ""):
                continue
            head_child = MemoryNode(str1)
            head_node.add_node(head_child,MemoryEdge.EDGE_CONTAIN)
            head_child.add_node(head_node,MemoryEdge.EDGE_RELATION)
            mm.add_node(head_child)
        tail_node = MemoryNode()
        for i in range(len(tail_list)):
            tail_unit = tail_list[i]
            str1 = ""
            for uunit in tail_unit:
                str1 = str1 + uunit[0]
            if(str1==""):
                continue
            tail_child = MemoryNode(str1)
            tail_node.add_node(tail_child, MemoryEdge.EDGE_CONTAIN)
            tail_child.add_node(head_node, MemoryEdge.EDGE_RELATION)
            mm.add_node(tail_child)
        str1 = ""
        for uunit in body:
            str1 = str1 + uunit[0]
        body_node = MemoryNode(str1)
        head_node.add_node(body_node)
        body_node.add_node(tail_node)
        mm.add_node(body_node)
        #mm.say()
        pass

    def mark_tail(self,row):
        arr = []
        flag = False
        for i in range(len(row)):
            if (row[i][2] == 1):
                flag = True
            else:
                if(flag and self.is_empty_value(row[i])==False):
                    arr.append(row[i])
        return arr

    def mark_head(self,row):
        arr = []
        for i in range(len(row)):
            if(row[i][2]==0):
                arr.append(row[i])
            else:
                break
        return arr

    def mark_body(self,row):
        arr = []
        for i in range(len(row)):
            if (row[i][2] == 1):
                arr.append(row[i])
        return arr

    def add_simple_node_chain(self,chain:SimpleNodeChain):
        cnode = chain.get_head()
        self.clear_column_index()
        row = self.get_row()
        while True:
            if(cnode==None):
                break
            self.set_row_value(row,cnode.value)
            cnode = cnode.get_next_node()
        self.set_next_row()

    def add_inner_data(self,inner_data:InnerData):
        self.clear_column_index()
        row = self.get_row()
        value = inner_data.value
        self.add_simple_node_chain(inner_data.value)

im = ImpressMain()