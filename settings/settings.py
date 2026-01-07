import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)



from photo_handler.limit_class import Limits
from enum import StrEnum

#screen params
weight, height = 640, 480

dp = 7 #delta pixels
da = 0 #delta degree

central_line_limit = Limits((weight, height), length=(200, 1000))


class Plates(StrEnum):
    manipulator = 'manipulator'
    wheels = 'wheels'
    undefined = 'undefined'

class Comands(StrEnum):
    getPlate = 'getPlate'
    moveForward = 'moveForward'
    moveBackward = 'moveBackward'
