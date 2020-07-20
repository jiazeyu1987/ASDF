import numpy as np
class ImpressMainPage:
    def __init__(self):
        self._width = 20
        self._height = 5
        self._depth = 3
        self._page_index = 0
        self._row_index = 0
        self._column_index = 0
        self.area = (np.zeros((self._depth, self._height,self._width), np.dtype([("value",np.str_,40),("type",np.int32),("mark",np.int32)])))


    def print_page(self):
        print(self.area[self._page_index])


    def get_row(self,index=-1):
        if(index==-1):
            return self.area[self._page_index][self._row_index]
        else:
            return self.area[self._page_index][index]

    def set_row_value(self,row,value):
        row[self._column_index] = (value,1,0)
        self.set_next_column()


    def is_empty_value(self,value):
        if(value[0]==''):
            return True
        return False


    def clear_column_index(self):
        self._column_index = 0

    def clear_row_index(self):
        self._row_index = 0

    def is_empty_row(self,row_index):
        for i in range(self._width):
            if(self.is_empty_value(self.area[self._page_index][row_index][i])):
                pass
            else:
                return False
        return True

    def get_compare_row(self):
        tmp_row_index = self._row_index
        tmp_arr = []
        while True:
            tmp_row_index-=1
            if(tmp_row_index<0):
                tmp_row_index = self._height-1
            if(tmp_row_index==self._row_index):
                break
            row = self.get_row(tmp_row_index)
            if(self.is_empty_row(tmp_row_index)):
                continue
            else:
                tmp_arr.append(row)
        return tmp_arr

    def get_past_row(self):
        self.clear_column_index()
        if (self._row_index - 1 == -1):
            self._row_index = self._height-1
        else:
            self._row_index -= 1

    def set_next_column(self):
        if (self._column_index + 1 == self._width):
            self._column_index = 0
        else:
            self._column_index += 1

    def set_next_row(self):
        self.clear_column_index()
        if (self._row_index + 1 == self._height):
            self._row_index = 0
        else:
            self._row_index += 1

    def set_next_page(self):
        self.clear_column_index()
        self.clear_row_index()
        if(self._page_index+1==self._depth):
            self._page_index = 0
        else:
            self._page_index+=1
        self.area[self._page_index] = (np.zeros((self._height,self._width), dtype=np.str))