import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)



from photo_handler.limit_class import Limits
from enum import StrEnum
import numpy as np
from datetime import timedelta

trash_frames = 5

#screen params
weight, height = 640, 480
cam_coef_sp = 5/160 #santimetrs/pixels
cam_coef_ps = 160/5 #pixels/santimetrs

dp = 7 #delta pixels
da = 0 #delta degree

#limits
central_line_limit = Limits((weight, height), length=(200, 1000))
x_grab_lim = 2.5#2.5
y_grab_lim = 2
cube_take_limit = Limits((weight, height), v_bounds=(0.5-(cam_coef_ps*x_grab_lim/weight), 0.5+(cam_coef_ps*x_grab_lim/weight)), h_bounds=(0.5-(cam_coef_ps*y_grab_lim/height), 0.5+(cam_coef_ps*y_grab_lim/height)))

rail_ground_limit = 16
rail_board_limit = 9
rail_zero_limit = 0

arduino_ver_step_limit = [0, 30]
arduino_hor_step_limit = [0, 47]
open_limit = 120
close_limit = 0

separator = '#' 
wait_arduino_define = timedelta(seconds=2)

hand_cam_id = 0
base_cam_id = 1

wait_card_delay = 10#seconds

#hsv (lower, upper)
class Color(StrEnum):
    red = 'red'
    blue = 'blue'
    yellow = 'yellow'
    white = 'white'

class Colors:
    def __init__(self, name: str, h: tuple, s: tuple, v: tuple):
        self.name = name
        self.lower = np.array([h[0], s[0], v[0]])
        self.upper = np.array([h[-1], s[-1], v[-1]])
    
    def __str__(self):
        return self.name
    
    def contains_h(self, h):
        return self.lower[0] <= h <= self.upper[0]
    
    def contains_s(self, s):
        return self.lower[1] <= s <= self.upper[1]
    
    def contains_v(self, v):
        return self.lower[-1] <= v <= self.upper[-1]
    
    def contains_hsv(self, h, s, v):
        return self.contains_h(h) and self.contains_s(s) and self.contains_v(v)
    
card_red_start = Colors(Color.red, (0, 10), (50, 255), (70, 255))
card_red_end = Colors(Color.red, (160, 180), (50, 255), (70, 255))
card_blue = Colors(Color.blue, (90, 128), (50, 255), (70, 255))
card_yellow = Colors(Color.yellow, (20, 35), (100, 255), (100, 255))

# cube_red_start = Colors(Color.red, (0, 50), (80, 255), (40, 255))
# cube_red_end = Colors(Color.red, (160, 180), (50, 255), (70, 255))
# cube_blue = Colors(Color.blue, (60, 179), (50, 255), (40, 255))
# cube_yellow = Colors(Color.yellow, (50, 100), (35, 255), (130, 255))
# cube_white = Colors(Color.white, (0, 50), (60, 100), (170, 255))

cube_red_start = Colors(Color.red, (0, 50), (100, 255), (40, 255))
cube_red_end = Colors(Color.red, (160, 180), (50, 255), (70, 255))
cube_blue = Colors(Color.blue, (101, 159), (50, 255), (40, 255))
cube_yellow = Colors(Color.yellow, (52, 100), (35, 255), (130, 255))
cube_white = Colors(Color.white, (0, 50), (60, 99), (170, 255))

background = Colors(Color.white, (25, 179), (0, 32), (100, 255))