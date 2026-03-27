from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.arduino_class import Arduino, get_available_ports
from robofest.classes.camera_class import Camera, flip, Flip
from robofest.classes.geometry_class import Point

from robofest.functions.center_handler import get_center_contour, get_storage_centers
from robofest.functions.lines_handler import handl_lines
from robofest.functions.math_funcs import get_step_angle, get_coords

from robofest.scenes.alignment_by_line import levelout_lines

import cv2

avaliable_ports = get_available_ports()
arduino = Arduino('COM4')

cam = Camera(1)

levelout_lines(cam, arduino, [87, 1, (1,1)])
# cv2.destroyAllWindows()
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break