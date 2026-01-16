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
    c = s.split('#')[0]
    arg = s.split('#')
    if c=='mf':
        wheels.move_forward_time(arg[0])
    elif c=='mb':
        wheels.move_backward_time(arg[0])
    elif c=='st':
        wheels.move_stop()
    elif c=='rt':
        manipulator.rotateRail(90)
    elif c=='chg':
        wheels.changeSpeed(arg[0], arg[1], arg[2], arg[3])

start = datetime.now()

wheels, manipulator = take_arduinos()
print(wheels)
print(manipulator)

inpt = input()
while inpt!='stop':
    c_f(inpt)
    inpt = input()

end = datetime.now()

print('total time:', end-start)