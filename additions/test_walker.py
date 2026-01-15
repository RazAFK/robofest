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

def c_f(s):
    c, arg = s.split('#')[0], s.split('#')[-1]
    if c=='moveForward':
        wheels.move_forward_time(arg)
    elif c=='stop':
        wheels.move_stop()

start = datetime.now()

wheels, manipulator = take_arduinos()
print(wheels)
print(manipulator)

inpt = input()
while inpt!='stp':
    c_f(inpt)
    inpt = input()

end = datetime.now()

print('total time:', end-start)