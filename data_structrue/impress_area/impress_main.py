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
        simple_node_chain.on_data_enter("天周日天气不错")
        self.add_simple_node_chain(simple_node_chain)
        #self.print_page()

        simple_node_chain = SimpleNodeChain()
        simple_node_chain.on_data_enter("图星期天天气不错")
        self.add_simple_node_chain(simple_node_chain)
        #self.print_page()

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
                print(unit_head,unit_tail)
                if(unit_tail[1]-unit_head[1]==1 and unit_tail[0]-unit_head[0]==1):
                    source_row[unit_head[0]][2]=1
                    source_row[unit_tail[0]][2] = 1
                    compare_row[unit_head[1]][2] = 1
                    compare_row[unit_tail[1]][2] = 1
        self.last_chain_index += 1
        return True


    def compare(self):
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
        print(self.result_arr)

        while True:
            r = self.chain_neighbor_unit(source_row,compare_row)
            if(r==False):
                break

        source_head = self.mark_head(source_row)
        compare_head = self.mark_head(compare_row)
        source_tail = self.mark_tail(source_row)
        compare_tail = self.mark_tail(compare_row)
        body = self.mark_body(source_row)
        self.save_to_brain([source_head,compare_head],body,[source_tail,compare_tail])

    def save_to_brain(self,source_list,body,tail_list):
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

