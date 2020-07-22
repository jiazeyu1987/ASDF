main = True

'''
    Print Relation
'''
log_map = {}
log_map["im"] =1
log_map["d1c"] =0
log_map["ft"] =0
log_map["nr"] = 0
def p(title,message):
    if(title in log_map):
        if(log_map[title]==1):
            print(message)

'''
    Read Relation
'''
time_gap = {}
time_gap_symbol = "墼"
sleep_symbol = "㮟"
replace_symbol = "甈"
entity_book_name = "./book/compare/compare1"
sound_book_name = "./book/sound.txt"
number_book_name = "./book/math/number.txt"
#单次处理的最大字符数
max_char_can_handle = 150
#经过如下数量的无聊代码还没有新的字符进入，那么执行剩余的charlist
max_time_gap_symbol_to_handle = 10


'''
    Personal Special
'''
#for low desire , max is 10
g_ps_desire_point = 1
'''
    FastNode 
'''
g_fn_add_weight_number = 1
g_fn_lose_weight_number = 1
g_fn_max_pool_deepth = 2
g_fn_search_depth = 5

'''
    D1Chainlist
'''
g_d1c_max_search_depth = 20

'''
    Memory
'''
g_mm_empty_symbol = "瀔"
