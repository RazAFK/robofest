import cv2

from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.camera_class import *
from robofest.classes.limit_class import Limits

from robofest.functions.lines_handler import handl_lines
from robofest.functions.drow_funcs import drow_lines, drow_limit, drow_lines_params
from robofest.functions.eco_utilities import get_average_between, Params



cam = Camera(1)

def nothing(x):
    pass

limit = Limits((st.wheels_width, st.wheels_height),
               distance=(0, 500),
               length=(0, 500),
               angle=(0, 90),
               x_bounds=(0, 1),
               y_bounds=(0, 1))

cv2.namedWindow('Settings')
cv2.createTrackbar('x_min', 'Settings', int(limit.x_min*100), 100, nothing)
cv2.createTrackbar('x_max', 'Settings', int(limit.x_max*100), 100, nothing)
cv2.createTrackbar('y_min', 'Settings', int(limit.y_min*100), 100, nothing)
cv2.createTrackbar('y_max', 'Settings', int(limit.y_max*100), 100, nothing)
cv2.createTrackbar('a_min', 'Settings', 90+limit.angle_min, 180, nothing)
cv2.createTrackbar('a_max', 'Settings', 90+limit.angle_max, 180, nothing)
cv2.createTrackbar('l_min', 'Settings', limit.length_min, 500, nothing)
cv2.createTrackbar('l_max', 'Settings', limit.length_max, 500, nothing)
cv2.createTrackbar('d_min', 'Settings', limit.distance_min, 500, nothing)
cv2.createTrackbar('d_max', 'Settings', limit.distance_max, 500, nothing)

cv2.namedWindow('Set')
cv2.resizeWindow('Set', 1920, 480)
cv2.createTrackbar('x_min', 'Set', 0, 640, nothing)
cv2.createTrackbar('x_max', 'Set', 640, 640, nothing)
cv2.createTrackbar('y_min', 'Set', 0, 480, nothing)
cv2.createTrackbar('y_max', 'Set', 480, 480, nothing)
cv2.createTrackbar('a_min', 'Set', 90+0, 180, nothing)
cv2.createTrackbar('a_max', 'Set', 90+90, 180, nothing)
cv2.createTrackbar('l_min', 'Set', 0, 500, nothing)
cv2.createTrackbar('l_max', 'Set', 500, 500, nothing)

old_limit = limit
index = 1
angles = []
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print('angle', sum(angles)/len(angles))
        break
    if key == ord('.'):
        if index>=68:
            index=0
        index += 1
    if key == ord(','):
        if index<=1:
            index=69
        index -= 1

    x_min = cv2.getTrackbarPos('x_min', 'Settings')/100
    x_max = cv2.getTrackbarPos('x_max', 'Settings')/100
    y_min = cv2.getTrackbarPos('y_min', 'Settings')/100
    y_max = cv2.getTrackbarPos('y_max', 'Settings')/100
    a_min = cv2.getTrackbarPos('a_min', 'Settings')-90
    a_max = cv2.getTrackbarPos('a_max', 'Settings')-90
    l_min = cv2.getTrackbarPos('l_min', 'Settings')
    l_max = cv2.getTrackbarPos('l_max', 'Settings')
    d_min = cv2.getTrackbarPos('d_min', 'Settings')
    d_max = cv2.getTrackbarPos('d_max', 'Settings')
    limit = Limits(
        (st.wheels_width, st.wheels_height),
        (d_min, d_max),
        (l_min, l_max),
        (a_min, a_max),
        (x_min, x_max),
        (y_min, y_max)
    )
    if not(old_limit==limit):
        old_limit=limit
        print(limit)
    frame = cam.get_frame()
    # frame = cv2.imread(f'C:/Users/admin/Desktop/line_photos/{index}.jpg')
    # frame = flip(frame, Flip.wheels)
    if frame is None: continue
    lines = handl_lines(frame, limit)
    result = drow_lines(frame, lines, (0, 0, 255))
    result = drow_limit(result, limit, (0, 255, 0))
    result = drow_lines_params(result, lines)
    x_n= cv2.getTrackbarPos('x_min', 'Set')/100
    x_x = cv2.getTrackbarPos('x_max', 'Set')/100
    y_n = cv2.getTrackbarPos('y_min', 'Set')/100
    y_x = cv2.getTrackbarPos('y_max', 'Set')/100
    a_n = cv2.getTrackbarPos('a_min', 'Set')-90
    a_x = cv2.getTrackbarPos('a_max', 'Set')-90
    l_n = cv2.getTrackbarPos('l_min', 'Set')
    l_x = cv2.getTrackbarPos('l_max', 'Set')
    angle = get_average_between(lines, Params.angle, angle=(a_min, a_max))
    if angle is not None:
        angles.append(angle)
    cv2.putText(result, f'length: {get_average_between(lines, Params.length, length=(l_min, l_max))}', (20, st.wheels_height-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(result, f'angle: {angle}', (20, st.wheels_height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(result, f'cord: {get_average_between(lines, Params.position, position=((x_min, x_max), (y_min, y_max)))}', (20, st.wheels_height-80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(result, f'{index}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if result is not None:
        cv2.imshow(f'result', result)
    cv2.imshow('frame', frame)