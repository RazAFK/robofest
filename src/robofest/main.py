from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.arduino_class import Arduino, get_available_ports
from robofest.classes.camera_class import Camera, flip, Flip
from robofest.classes.reader_class import Reader
from robofest.classes.geometry_class import Point
from robofest.classes.limit_class import Limits
from robofest.classes.pid_class import PID

from robofest.functions.center_handler import get_center_contour, get_storage_centers
from robofest.functions.lines_handler import handl_lines
from robofest.functions.num_handler import handl_num
from robofest.functions.math_funcs import get_step_angle, get_coords

from robofest.scenes.alignment import levelout_angle

import time, cv2

avaliable_ports = get_available_ports()
arduino = Arduino(avaliable_ports[0])

arduino.arm.rotate_manipulator(90)
reader = Reader()

arm_cam = Camera(st.arm_id)
wheel_cam = Camera(1)
frame = wheel_cam.get_frame()
cv2.imshow('frame', frame)

pid = PID(kp=0.0004, ki=0.000, kd=0.000, admission=0.05)

time.sleep(1)
limit = Limits(sizes=(st.wheels_width, st.wheels_height), length=(150, 1000), angle=(0, 90), x_bounds=(0, 0.7))

start = time.time()
levelout_angle(wheel_cam, arduino, 90, limit, pid)
print(time.time()-start)