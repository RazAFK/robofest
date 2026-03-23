from robofest.settings import settings as st

from robofest.classes.camera_class import Camera, Flip, flip
from robofest.classes.limit_class import Limits
from robofest.classes.arduino_class import Arduino

from robofest.functions.lines_handler import handl_lines, handl_lines_by

from datetime import datetime

def levelout_lines(cam: Camera, limit: Limits, arduino: Arduino, line_count: int, cam_flip: Flip = Flip.wheels):
    arduino.whe.rotate_right(2)

    move_flag = True

    while move_flag:
        frame = flip(cam.get_frame(), cam_flip)
        lines = handl_lines(frame, limit)
        if len(lines)==line_count:
            move_flag = False

    while move_flag:
        frame = flip(cam.get_frame(), cam_flip)
        lines = handl_lines(frame, limit)
        if len(lines)==line_count:
            move_flag = False
    

    

