import cv2

from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.camera_class import *
from robofest.classes.reader_class import Reader
from robofest.classes.limit_class import Limits

from robofest.functions.num_handler import handl_num
from robofest.functions.lines_handler import handl_lines
from robofest.functions.drow_funcs import drow_lines, drow_limit, drow_lines_angles
from robofest.functions.initialyzation_funcs import init_arduino


# arm, arm_q, wheels, wheels_q = init_arduino()
# print(arm, wheels)

arm_cam = Camera(0)

def nothing(x):
    pass

limit = Limits((st.wheels_width, st.wheels_height),
               (0, 1000),
               (-90, 90),
               (0, 1),
               (0, 1))

cv2.namedWindow('Settings')
cv2.createTrackbar('x_min', 'Settings', int(limit.x_min*100), 100, nothing)
cv2.createTrackbar('x_max', 'Settings', int(limit.x_max*100), 100, nothing)
cv2.createTrackbar('y_min', 'Settings', int(limit.y_min*100), 100, nothing)
cv2.createTrackbar('y_max', 'Settings', int(limit.y_max*100), 100, nothing)
cv2.createTrackbar('a_min', 'Settings', 90+limit.angle_min, 180, nothing)
cv2.createTrackbar('a_max', 'Settings', 90+limit.angle_max, 180, nothing)
cv2.createTrackbar('l_min', 'Settings', limit.length_min, 500, nothing)

old_limit = limit

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    x_min = cv2.getTrackbarPos('x_min', 'Settings')/100
    x_max = cv2.getTrackbarPos('x_max', 'Settings')/100
    y_min = cv2.getTrackbarPos('y_min', 'Settings')/100
    y_max = cv2.getTrackbarPos('y_max', 'Settings')/100
    a_min = cv2.getTrackbarPos('a_min', 'Settings')-90
    a_max = cv2.getTrackbarPos('a_max', 'Settings')-90
    l_min = cv2.getTrackbarPos('l_min', 'Settings')
    l_max = 500
    limit = Limits(
        (st.wheels_width, st.wheels_height),
        (l_min, l_max),
        (a_min, a_max),
        (x_min, x_max),
        (y_min, y_max)
    )
    if not(old_limit==limit):
        old_limit=limit
        print(limit)
    frame = arm_cam.get_frame()
    frame = flip(frame, Flip.wheels)
    if frame is None: continue
    lines = handl_lines(frame, limit)
    result = drow_lines(frame, lines, (0, 0, 255))
    result = drow_limit(result, limit, (0, 255, 0))
    result = drow_lines_angles(result, lines)
    if result is not None:
        cv2.imshow(f'result', result)
    cv2.imshow('frame', frame)