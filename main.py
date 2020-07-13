import action as ac
from queue import Queue
#ac.init()
import receiver as rv
queue = Queue()
t1 = rv.Eye(queue)
t2 = rv.NumberReceiver(queue)
t1.start()
t2.start()
t1.join()
t2.join()