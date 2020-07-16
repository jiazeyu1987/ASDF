import action as ac
from queue import Queue
import data_structrue as ds
ac.init()
import receiver as rv
out_string_queue = Queue()
inner_message_queue = Queue()
t1 = rv.Eye(out_string_queue)
t1.start()


t2 = rv.NumberReceiver(out_string_queue,inner_message_queue)
t2.start()

fast_tree = ds.FastTree(inner_message_queue)
#fast_tree.start()
#fast_tree.join()

chain_list = ds.ChainListMain(inner_message_queue,fast_tree)
chain_list.start()

t1.join()
t2.join()
chain_list.join()




