import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)



from photo_handler.limit_class import *
weight, height = 640, 480
w, h = 640, 480
central_line_limit = Limits((h, w), length=(200, 1000))

dp = 7 #pixels
da = 0 #degree