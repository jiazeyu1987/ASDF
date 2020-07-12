import globalconfig as g
from receiver.local_reader import *
class BuildinReadSound:
    def __init__(self):
        pass

    def load(self):
        book_string_raw = read_file(g.sound_book_name)
        gap_string = change_raw_string_to_gap_string(book_string_raw)
        index = 0
        unitlist = []
        while True:
            target_string,gap_string = split_gap_string_by_gap_number(gap_string,3)
            if(len(target_string)>0):
                unitlist.append(target_string)
            if(len(gap_string)==0):
                break
        index = 0
        for unit in unitlist:
            strlist1 = str.split(unit,g.time_gap_symbol)
            if(len(strlist1)!=2):
                continue
            index+=1
            value = strlist1[0]
            key = strlist1[1]
            diao = key[-1]
            pinyin = key[0:len(key)-1]
            print(value,diao,pinyin)
        print(index)
brs = BuildinReadSound()