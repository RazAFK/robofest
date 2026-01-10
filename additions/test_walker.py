import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

from connector.arduino_class import *
from datetime import datetime
import queue, threading

# data_queue = queue.Queue()

# data_queue.put(item)
# data_queue.get()

start = datetime.now()

wheels, manipulator = take_arduinos()

wheels.move_forward_time(15000)

end = datetime.now()

print('total time:', end-start)