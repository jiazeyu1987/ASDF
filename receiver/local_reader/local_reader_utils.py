#file_name：'D:/story/灰姑娘.txt'
def read_file(file_name):
    f = ''
    try:
        f = open(file_name, 'r', encoding='utf-8')
        return f.read()
    finally:
        if f:
            f.close()

# raw_string
# 0,
# 1,
# 2,
# 3,
# 4,
# 5,
# 6,
# 7,
# 8,
# 9,
# 10,
# 11,
# 12,
# 13,

# return:0           1           2           3           4           5           6           7           8           9           10           11           12           13
# 将未统一的字符串转化为统一的字符串
import globalconfig as g
def change_raw_string_to_gap_string(raw_string):
    gap_string = ""
    for char in raw_string:
        if(char in g.time_gap):
            gap_number = g.time_gap.get(char)
            for i in range(gap_number):
                gap_string = gap_string+g.time_gap_symbol
        else:
            gap_string = gap_string+char
    return gap_string


#从gap_string中提取需要的信息
#gap_number gap_number表示提取的空白符号的长度
#比如说 1 A   2 B   3 C   4 D   5 E
#gap_number=1,返回值为1,A   2 B   3 C   4 D   5 E
#gap_number>1,返回值为1 A，2 B   3 C   4 D   5 E
def split_gap_string_by_gap_number(gap_string,gap_number):
    if(len(gap_string)==0):
        return "",""
    for i in range(len(gap_string)):
        char = gap_string[i]
        if(char == g.time_gap_symbol):
            index = 0
            for j in range(i+1,len(gap_string)):
                if(gap_string[j] == g.time_gap_symbol):
                    index+=1
                    continue
                else:
                    break
            if(index==len(gap_string)-1):
                return "",""
            if(index+1>gap_number-1):
                return gap_string[:i],gap_string[j:len(gap_string)]
    return gap_string,""

#将gapstring从最大的gap分开
#PS 0 ling2          1 yi1          2 er4          3 san1          4 si4          5 wu3          6 liu4          7 qi1          8 ba1          9 jiu3          10 shi2
#返回 0 ling2:1 yi1          2 er4          3 san1          4 si4          5 wu3          6 liu4          7 qi1          8 ba1          9 jiu3          10 shi2

def split_gap_string_by_larger_gap(gap_string):
    largest_index = -1
    lagest_number = -1
    larger_number = 0
    for i in range(len(gap_string)):
        char = gap_string[i]
        if(char == g.time_gap_symbol):
            larger_number = 1
            for j in range(i+1,len(gap_string)):
                if(gap_string[j]==g.time_gap_symbol):
                    larger_number+=1
                else:
                    break
            if(larger_number>lagest_number):
                lagest_number = larger_number
                largest_index = i
    if(largest_index!=-1):
        return gap_string[0:largest_index],gap_string[(largest_index+lagest_number):len(gap_string)]
