import threading
from headcounter import headcounter
import time
import numpy as np

hct = headcounter()
lock = threading.Lock()
path = 'vid.mp4'
vertexes = np.array([(0, 372//2), (250, 372//3), (499, 372//2), (499, 372), (0, 372)])
t1 = threading.Thread(target=hct.run, args=(lock, path, vertexes))
t1.start()
time.sleep(5)
lock.acquire()
hct.stop = True
lock.release()