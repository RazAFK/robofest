import cv2
from datetime import datetime as timer
from datetime import timedelta

from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.camera_class import *
from robofest.classes.reader_class import Reader
from robofest.classes.geometry_class import Point

from robofest.functions.num_handler import handl_num
from robofest.functions.lines_handler import handl_lines
from robofest.functions.drow_funcs import drow_lines, drow_limit
from robofest.functions.initialyzation_funcs import init_arduino
from robofest.functions.center_handler import get_center_contour, get_storage_centers
from robofest.functions.utilities import remath_cords


def drow_center_dot(img):
    cv2.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 4, (0, 255, 0), -1)
    return img

def use_decor(s: set, img):
    for func in s:
        if func==drow_limit:
            img = func(img, lst.limit_grab_cube)
        else:
            img = func(img)
    return img



arm, arm_q, wheels, wheels_q = init_arduino()
print(arm, wheels)

arm_cam = Camera(0)

reader = Reader()


arm.move_arm(10, 0)



# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     frame = arm_cam.get_frame()
#     frame = flip(frame, Flip.hand)
#     if frame is None: continue
#     result = drow_limit(frame, lst.limit_grab_cube)
#     if result is not None:
#         cv2.imshow('result', result)
#     cv2.imshow('frame', frame)




old_cords = None
new_cords = None
result = None
finding_flag = False
storage_flag = False
move_flag = False
grab_flag = False
center_dot = False
limit_dots = False
limits = False
last_start = timer.now()
i=1

def nothing(x):
    pass

cv2.namedWindow('Settings')
cv2.createTrackbar('x', 'Settings', 0, 60, nothing)
cv2.createTrackbar('y', 'Settings', 0, 30, nothing)

decorators = set()

while True:
    
    frame = arm_cam.get_frame()
    frame = flip(frame, Flip.hand)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w') and not storage_flag:
        finding_flag = not(finding_flag)
        print('finding_flag:', finding_flag)

    elif key == ord('z') and not finding_flag:
        storage_flag = not(storage_flag)
        print('storage_flag:', storage_flag)

    elif key == ord('e'):
        x = cv2.getTrackbarPos('x', 'Settings')
        y = cv2.getTrackbarPos('y', 'Settings')
        arm.move_arm(x, y)
        move_flag = True

    elif key == ord('a'):
        if not center_dot:
            try:
                decorators.remove(drow_center_dot)
            except: pass
        else:
            decorators.add(drow_center_dot)
        print('center dot:', center_dot)
        center_dot = not(center_dot)
    
    elif key == ord('s'):
        if not limit_dots:
            try:
                decorators.remove(drow_limit)
            except: pass
        else:
            decorators.add(drow_limit)
        print('limit dots:', limit_dots)
        limit_dots = not(limit_dots)

    if result is not None:
        result = use_decor(decorators, result)
        cv2.imshow('result', result)
    frame = use_decor(decorators, frame)
    cv2.imshow('frame', frame)

    data = arm_q.get_data()
    if data and data.check_state(st.Prefixes.moveDone):
        arm.get_coordinates()
        move_flag = False
    if data and data.check_state(st.Prefixes.cords):
        old_cords = Point(*list(map(int, data.args)))
    if old_cords is not None:
        if finding_flag:
            ret, data = get_center_contour(frame)
            if not ret: continue
            cX, cY = data[0]
            cnt = data[1]
            result = data[-1].copy()
            file = data[-1].copy()
            area = cv2.contourArea(cnt)
            
            cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(result, f"Area: {int(area)}", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
        elif storage_flag:
            centers = get_storage_centers(frame, reader)
            ml = 0
            cX, cY = old_cords.x, old_cords.y
            for center in centers:
                cords, text, conf, result = center
                x, y = cords
                l = st.hypot(old_cords, Point(x, y))
                if l<ml:
                    ml=l
                    cX, cY = cords
            if cX!=old_cords.x and cY!=old_cords.y:
                cv2.circle(result, (cX, cY), 5, (0, 255, 0), -1)
                cv2.putText(result, f'{text}, {conf}', (cX - 20, cY - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
        if  (storage_flag or finding_flag) and (cX!=old_cords.x and cY!=old_cords.y):
            h = result.shape[0]
            w = result.shape[1]
            new_cords = remath_cords((old_cords.x, old_cords.y), (cX, cY), (w/2, h/2))
            new_cords = Point(int(new_cords[0]), int(new_cords[-1]))
            if lst.limit_grab_cube.contains_point(new_cords):
                new_cords = None

    if new_cords is not None and not move_flag and timer.now()-last_start>=timedelta(seconds=3):
        arm.move_arm(new_cords.x, new_cords.y)
        last_start = timer.now()
        new_cords = None
        move_flag = True