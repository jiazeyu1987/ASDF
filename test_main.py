
from queue import Queue
import  queue
import data_structrue as ds
import globalconfig as g
def test():
    g.time_gap[","] = 1
    g.time_gap["."] = 3
    g.time_gap[";"] = 2
    g.time_gap["，"] = 1
    g.time_gap["；"] = 2
    g.time_gap["。"] = 3
    g.time_gap[" "] = 1
    g.time_gap["\t"] = 3
    g.time_gap["\n"] = 5
    g.time_gap[','] = 1
    g.time_gap['.'] = 3
    g.time_gap[';'] = 2
    g.time_gap['，'] = 1
    g.time_gap['；'] = 2
    g.time_gap['。'] = 3
    g.time_gap[' '] = 1
    g.time_gap['\t'] = 3
    g.time_gap['\n'] = 5

    import receiver as rv
    out_string_queue = Queue()
    d1_message_queue = Queue()
    d2_message_queue = Queue()
    exception_queue = Queue()
    t1 = rv.Eye(out_string_queue)
    t1.start()


    t2 = rv.NumberReceiver(out_string_queue,d1_message_queue)
    t2.start()

    fast_tree = ds.FastTree(d1_message_queue)

    d1chain_list = ds.D1ChainList(d1_message_queue,fast_tree,exception_queue)
    d1chain_list.start()


    t1.join()
    t2.join()
    d1chain_list.join()

    while g.main:
        import sys,traceback
        try:
            exc = exception_queue.get(block=False)
        except queue.Empty:
            break
        else:
            exc_type, exc_obj, exc_trace = exc
            traceback.print_exception(exc_type, exc_obj, exc_trace)



