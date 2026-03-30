from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.arduino_class import Arduino, get_available_ports
from robofest.classes.camera_class import Camera, flip, Flip
# from robofest.classes.reader_class import Reader
from robofest.classes.geometry_class import Point
from robofest.classes.limit_class import Limits
from robofest.classes.pid_class import PID

from robofest.functions.center_handler import get_center_contour, get_storage_centers
from robofest.functions.lines_handler import handl_lines
# from robofest.functions.num_handler import handl_num
from robofest.functions.math_funcs import get_step_angle, get_coords

from robofest.scenes.alignment import levelout_angle

import time, cv2

avaliable_ports = get_available_ports()
arduino = Arduino(avaliable_ports[0])
print(f'[INFO] ардуино на порту {arduino.port}')

# arduino.arm.rotate_manipulator(90)
# reader = Reader()

# arm_cam = Camera(0)
# wheel_cam = Camera(1)
# frame = wheel_cam.get_frame()

# print(f'[INFO] всё работает')
# cv2.imshow('wheels', frame)
# camera = input('is it wheels camera? Y/n')
# if camera.lower()!='y':
#     wheel_cam, arm_cam = arm_cam, wheel_cam
# start = time.time()
# while time.time()-start<10:
#     frame = wheel_cam.get_frame()
#     # result = handl_num(frame, reader)
#     if result is not None:
#         print(f'[INFO] я увидел номер {result[0]} на {result[1]} фоне')


# pid = PID(kp=0.0004, ki=0.000, kd=0.000, admission=0.05)
# levelout_limit = Limits(sizes=(st.wheels_width, st.wheels_height), length=(150, 1000), angle=(0, 90), x_bounds=(0, 0.8))

arduino.arm.rotate_grab_servo(90)
arduino.arm.rotate_horizontal_rail(180)
arduino.arm.rotate_manipulator(180)

arduino.whe.rotate_left(0.45)
arduino.wait_done()
arduino.whe.move_forward_distance(0.6)
arduino.wait_done()
arduino.whe.rotate_right(0.45)
arduino.wait_done()
arduino.whe.move_forward_distance(0.4)
arduino.wait_done()
arduino.whe.move_right(0.225)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_left(0.45)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_left(0.225)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_left(0.225)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_left(0.45)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_right(0.225)
arduino.wait_done()
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()

arduino.whe.move_forward_distance(0.5)
arduino.wait_done()
arduino.whe.move_forward_distance(0.5)
arduino.wait_done()
arduino.whe.move_forward_distance(0.5)
arduino.wait_done()
time.sleep(2.1)
arduino.whe.move_forward_distance(0.25)
arduino.wait_done()
arduino.whe.rotate_right(0.45)
arduino.wait_done()
arduino.whe.move_forward_distance(0.5)
arduino.wait_done()
# arduino.arm.rotate_horizontal_rail(90)
# arduino.wait_done()
# arduino.arm.move_horizontal_rail(1200)
# arduino.wait_done()
# arduino.arm.rotate_manipulator(90)
# arduino.wait_done()
# arduino.arm.rotate_grab_servo(120)
# arduino.wait_done()
# arm_cam.trash_frames(5)

# while True:
#     frame = arm_cam.get_frame()
#     ret, result = get_center_contour(frame)
#     if not ret:
#         continue
#     if lst.limit_grab_cube.contains_point(Point(result[0][0], result[0][-1])):
#         break
#     steps, angle, length = get_step_angle(result[0][0], result[0][-1])
#     arduino.arm.move_manipulator(steps, angle, if angle)
    


# start = time.time()
# levelout_angle(wheel_cam, arduino, 90, levelout_limit, pid)
# print(time.time()-start)