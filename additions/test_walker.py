import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

from settings.settings import Plates
from connector.arduino_class import *
from datetime import datetime

start = datetime.now()

wheels, manipulator = take_arduinos()

end = datetime.now()

print('total time:', end-start)