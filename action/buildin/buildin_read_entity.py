import globalconfig as g
from receiver.local_reader import *
class BuildinReadAction:
    def __init__(self):
        pass

    def load(self):
        book_string_raw = read_file(g.sound_book_name)
        gap_string = change_raw_string_to_gap_string(book_string_raw)
        target_string,gap_string = split_gap_string_by_larger_gap(gap_string)
        print(target_string+":"+gap_string)
        #target_string, gap_string = split_gap_string_by_larger_gap(gap_string)
        #print(target_string + ":" + gap_string)

bre = BuildinReadAction()