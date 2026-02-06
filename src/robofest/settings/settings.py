import datetime
from enum import StrEnum

#arduino queue
class Prefixes(StrEnum):
    data = 'data'
    moveDone = 'moveDone'
    cords = 'cords'

separator = '#'

queue_size = 5

#arduino init
arduino_baudrate=9600
arduino_timeout=0.1

wait_arduino_define = datetime.timedelta(seconds=2)


#camera
cap_width = 640
cap_height = 480

arm_width = cap_height
arm_height = cap_width

wheels_width = cap_width
wheels_height = cap_height

trash_frames = 3

cam_coef_san_pix = 5/147 #santimetrs/pixels
cam_coef_pix_san = 147/5 #pixels/santimetrs

#limits

limit_manipulator_open = 120
limit_manipulator_close = 0

limit_vertical_step = [0, 30]
limit_horizontal_step = [0, 47]

limit_min_area_num = 10_000
limit_min_area_cube = 60_000


#delta

delta_angle = 0 
delta_pixels = 7

delta_grab_x = 2.5
delta_grab_y = 2

#reader
reader_alf = '12345'

#robot
robot_radius = 45
robot_short_side = 26