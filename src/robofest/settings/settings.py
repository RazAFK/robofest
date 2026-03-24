import datetime, math
from enum import StrEnum

#arduino queue
class Prefixes(StrEnum):
    data = 'data'
    move_done = 'moveDone'
    cords = 'cords'

separator = '#'

queue_size = 5
queue_delay = 0

#arduino init
arduino_baudrate = 9600
arduino_timeout = 0.1
arduino_init_delay = 2

wait_arduino_define = datetime.timedelta(seconds=2)


#camera
cap_width = 640
cap_height = 480

arm_id = 0
arm_width = cap_height
arm_height = cap_width

wheel_id = 1
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

limit_horizontal_lenght_min = 10.005972601683492 #santimetrs
limit_horizontal_lenght_max = 99.99689416376313 #santimetrs
limit_horizontal_angle_min = 0 #degrees
limit_horizontal_angle_max = 270 #degrees

limit_min_area_num = 10_000 #pixels
limit_min_area_cube = 60_000 #pixels


#delta

delta_angle = 0 
delta_pixels = 7

delta_grab_x = 2.5 #santimetrs
delta_grab_y = 2 #santimetrs

#reader
reader_alf = '12345'

#robot

stepper_step = 1.8 #degrees
rail_horisontal_gear_D = 0.96 #santimetrs
rail_step = rail_horisontal_gear_D*math.pi*(stepper_step/360) #santimetrs
rail_center_offset_x = 100 #santimetrs
rail_center_offset_y = 100 #santimetrs

rail_angle_step = 1


velocity_front_right = 0.3
velocity_front_left = 0.3
velocity_backward_right = 0.3
velocity_backward_left = 0.3

robot_radius = math.sqrt(2)*0.15#metrs


#time
wait_card = datetime.timedelta(seconds=30)