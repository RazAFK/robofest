import cv2
import numpy as np
from time import sleep
from datetime import datetime as timer
from datetime import timedelta
import threading
import queue

from photo_handler.line_class import *
from photo_handler.camera_class import *
#from photo_handler.num_handler import handl_num
from photo_handler.block_handler import get_center_contour, is_special_color, remath_cords

from connector.arduino_class import *

import settings.settings as st

def drow_center_dot(img):
    cv2.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 4, (0, 255, 0), -1)
    return img

def drow_limit_dots(img):
    h = int(img.shape[0])
    w = int(img.shape[1])
    for x in range(0, int(img.shape[0])):
        for y in range(0, int(img.shape[1])):
            p = Point(x, y)
            if st.cube_take_limit.contains_p_wh(p, w, h):
                cv2.circle(img, (p.x, p.y), 4, (0, 255, 0), -1)
    return img

def drow_limit(img):
    h = int(img.shape[0])
    w = int(img.shape[1])
    #red | |
    cv2.line(img, (int(st.cube_take_limit.v_bounds[0]*w), 0), (int(st.cube_take_limit.v_bounds[0]*w), h), (0, 0, 255), 2)
    cv2.line(img, (int(st.cube_take_limit.v_bounds[-1]*w), 0), (int(st.cube_take_limit.v_bounds[-1]*w), h), (0, 0, 255), 2)
    # green =
    cv2.line(img, (0, int(st.cube_take_limit.h_bounds[0]*h)), (w, int(st.cube_take_limit.h_bounds[0]*h)), (0, 255, 0), 2)
    cv2.line(img, (0, int(st.cube_take_limit.h_bounds[-1]*h)), (w, int(st.cube_take_limit.h_bounds[-1]*h)), (0, 255, 0), 2)
    return img

def use_decor(s: set, img):
    for func in s:
        img = func(img)
    return img

wheels, manipulator = take_arduinos()
print(wheels, manipulator)

# wheels_queue = Queue(wheels)
# wheels_queue.start_thread()
hand_queue = Queue(manipulator)
hand_queue.start_thread()

hand_cam = Camera(st.hand_cam_id)

# base_cam = Camera(st.base_cam_id)
# base_cam, hand_cam = define_cam(base_cam, hand_cam)

manipulator.moveManipulator(0, 0)

old_cords = None
new_cords = None
result = None
finding_flag = False
move_flag = False
grab_flag = False
center_dot = False
limit_dots = False
limits = False
last_start = timer.now()

def nothing(x):
    pass

cv2.namedWindow('Settings')
cv2.createTrackbar('x', 'Settings', 0, 60, nothing)
cv2.createTrackbar('y', 'Settings', 0, 30, nothing)

decorators = set()

while True:
    
    frame = hand_cam.get_frame(Flip.hand)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        finding_flag = not(finding_flag)
        print('finding_flag:', finding_flag)

    elif key == ord('e'):
        x = cv2.getTrackbarPos('x', 'Settings')
        y = cv2.getTrackbarPos('y', 'Settings')
        manipulator.moveManipulator(x, y)
        move_flag = True
    
    elif key == ord('r'):
        manipulator.grabManipulator(False)
        time.sleep(0.5)
        manipulator.moveVerRail(16)
        time.sleep(0.5)
        manipulator.grabManipulator(True)
        time.sleep(0.5)
        manipulator.moveVerRail(0)
        time.sleep(0.5)
        # grab_flag=True

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
                decorators.remove(drow_limit_dots)
            except: pass
        else:
            decorators.add(drow_limit_dots)
        print('limit dots:', limit_dots)
        limit_dots = not(limit_dots)
    
    elif key == ord('d'):
        if not limits:
            try:
                decorators.remove(drow_limit)
            except: pass
        else:
            decorators.add(drow_limit)
        print('limits:', limits)
        limits = not(limits)

    if result is not None:
        result = use_decor(decorators, result)
        cv2.imshow('result', result)
    frame = use_decor(decorators, frame)
    cv2.imshow('frame', frame)

    data = hand_queue.get_data_nowait()

    if data and data.check_state(States.moveDone):
        if grab_flag:
            manipulator.grab()
            grab_flag=False
        else:
            manipulator.getCoordinates()
            move_flag = False
    if data and data.check_state(States.cords):
        old_cords = Point(*list(map(int, data.args)))
    if old_cords is not None:
        if finding_flag:
            ret, data = get_center_contour(hand_cam)
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
            h = result.shape[0]
            w = result.shape[1]
            new_cords = remath_cords((old_cords.x, old_cords.y), (cX, cY), (w/2, h/2))
            new_cords = Point(int(new_cords[0]), int(new_cords[-1]))
            if st.cube_take_limit.contains_p(new_cords):
                new_cords = None
                # grab_flag = True
    if new_cords is not None and not move_flag and timer.now()-last_start>=timedelta(seconds=3):
        manipulator.moveManipulator(new_cords.x, new_cords.y)
        last_start = timer.now()
        new_cords = None
        move_flag = True


# finding_flag = False
# i=1
# #platform 9
# #floor 16
# while True:



#     frame = hand_cam.get_frame(flip=Flip.hand)
#     cv2.imshow('frame', frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     elif key == ord('e'):
#         finding_flag = not(finding_flag)
#         print('finding_flag:', finding_flag)

    
#     elif key == ord('r'):
#         manipulator.reset()
#         if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
#             old_cords = manipulator.getCoordinates()

#     elif key == ord('z'):
#         manipulator.moveVerRail(16)
    
#     elif key == ord('x'):
#         manipulator.moveVerRail(9)
    
#     elif key == ord('c'):
#         manipulator.moveVerRail(-100)
    
#     elif key == ord('b'):
#         manipulator.grabManipulator(False)

#     elif key == ord('m'):
#         manipulator.grabManipulator(True)

#     elif key == ord('1'):
#         manipulator.moveManipulator(0, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 0 0', old_cords)
#     elif key == ord('2'):
#         manipulator.moveManipulator(10, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 10 0', old_cords)
#     elif key == ord('3'):
#         manipulator.moveManipulator(20, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 20 0', old_cords)
#     elif key == ord('4'):
#         manipulator.moveManipulator(30, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 30 0', old_cords)
#     elif key == ord('5'):
#         manipulator.moveManipulator(40, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 40 0', old_cords)
#     elif key == ord('6'):
#         manipulator.moveManipulator(50, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 50 0', old_cords)
#     elif key == ord('7'):
#         manipulator.moveManipulator(60, 0)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 60 0', old_cords)
#     elif key == ord('8'):
#         manipulator.moveManipulator(35, 20)
#         if 'moveDone' in  str(manipulator.get_data()):
#             old_cords = manipulator.getCoordinates()
#             print('SPECIAL 35 20', old_cords)

#     ret, data = get_center_contour(hand_cam)
#     if not ret: continue

#     new_cords = (old_cords.x, old_cords.y)

#     if finding_flag:
#         cX, cY = data[0]
#         cnt = data[1]
#         result = data[-1].copy()
#         file = data[-1].copy()
#         area = cv2.contourArea(cnt)
        
#         cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
#         cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
#         cv2.putText(result, f"Area: {int(area)}", (cX - 20, cY - 20),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
#         cv2.imshow('result', result)

#         new_cords = remath_cords((old_cords.x, old_cords.y), (cX, cY))
#         new_cords = (int(new_cords[0]), int(new_cords[-1]))
#         print('calculated cords', new_cords)
#         # if not st.cube_take_limit.contains_p(Point(*new_cords)): continue

#     if key == ord('s'):
#         cv2.imwrite(f'additions/photos/cubs/{i}.jpg', file)
#         cv2.imwrite(f'additions/photos/cubs/{i}_processed.jpg', result)
#         i+=1
    
#     print('old cords', old_cords)
#     if old_cords.x==new_cords[0] and old_cords.y==new_cords[-1]: continue
#     print('new cords', new_cords)
#     manipulator.moveManipulator(*new_cords)
#     if 'moveDone' in  str(manipulator.get_data()):
#         old_cords = manipulator.getCoordinates()
#     print('new old cords', old_cords)





# manipulator.moveManipulator(0, 0)
# sleep(2)
# manipulator.moveManipulator(5, 5)
# sleep(2)
# manipulator.moveManipulator(10, 10)
# sleep(2)
# manipulator.moveManipulator(0, 10)
# sleep(2)


# old_cords = manipulator.moveManipulator(20, 0)

# start_flag = True
# i=1

# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
#     if key == ord('f'):
#         old_cords = manipulator.moveManipulator(0, 0)
#     ret, data = get_center_contour(hand_cam)
#     if not ret: continue

#     cX, cY = data[0]
#     cnt = data[1]
#     result = data[-1].copy()
#     file = data[-1].copy()
#     area = cv2.contourArea(cnt)

#     cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
#     cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
#     cv2.putText(result, f"Area: {int(area)}", (cX - 20, cY - 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    

#     if key == ord('s'):
#         cv2.imwrite(f'additions/photos/cubs/{i}.jpg', file)
#         cv2.imwrite(f'additions/photos/cubs/{i}_processed.jpg', result)
#         i+=1

#     new_cords = remath_cords(old_cords, (cX, cY))
#     new_cords = (int(new_cords[0]), int(new_cords[-1]))

#     cv2.imshow('result', result)

#     if start_flag or timer.now()-start>=timedelta(seconds=5):
#         start_flag=False
#         print(*new_cords)
#         manipulator.moveManipulator(*new_cords)
#         old_cords = new_cords
#         start = timer.now()




# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#             break
#     ret, data = get_center_contour(hand_cam)
#     if not ret: continue
#     cX, cY = data[0]
#     cnt = data[1]
#     result = data[-1].copy()
#     area = cv2.contourArea(cnt)
#     color = is_special_color(result, cnt, st.cube_blue)
    
#     cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
#     cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
#     cv2.putText(result, f"Area: {int(area)}, Color: {color}", (cX - 20, cY - 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#     cv2.imshow('result', result)

#print(wheels, manipulator, hand_cam, base_cam)

# start = timer.now()
# while start-timer.now()<=timedelta(seconds=st.wait_card_delay):
#     num, color = handl_num(base_cam)
#     if num!=0 and color!=None:
#         print(num, color)
#         break

# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#             break
#     frame = cam.get_frame()
#     edges = cam.process_frame_top(frame)
#     lines = cam.get_lines(edges)
#     lines = cam.process_lines(lines, st.central_line_limit)
#     result = cam.drow_lines(frame, lines)
#     cv2.imshow('result', result)

# segment, percent = process_frame_after_stop(base_cam, Limits(sizes=(st.weight, st.height), v_bounds=(0.4, 0.6), angle=(-10, 10)))

# frame = cv2.flip(base_cam.get_frame(), -1)
# res = base_cam.process_frame_top(frame)
# result = base_cam.drow_lines(frame, [segment]) if segment is not None else frame
# print(percent)
# while True:
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#             break
#     cv2.imshow('res', res)
#     cv2.imshow('result', result)

# base_cam.cap.release()
hand_cam.cap.release()
cv2.destroyAllWindows()