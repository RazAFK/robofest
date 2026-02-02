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

wheels, manipulator = take_arduinos()
print(wheels, manipulator)

hand_cam = Camera(st.hand_cam_id)

# base_cam = Camera(st.base_cam_id)
# base_cam, hand_cam = define_cam(base_cam, hand_cam)

manipulator.moveManipulator(0, 0)
old_cords = Point(0, 0)


if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
    old_cords = manipulator.getCoordinates()

print(old_cords)

start_flag = True
finding_flag = False
i=1
#platform 9
#floor 16
while True:
    frame = hand_cam.get_frame(flip=Flip.hand)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        finding_flag = not(finding_flag)
        print('finding_flag:', finding_flag)

    
    elif key == ord('r'):
        manipulator.reset()
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()

    elif key == ord('z'):
        manipulator.moveVerRail(16)
    
    elif key == ord('x'):
        manipulator.moveVerRail(9)
    
    elif key == ord('c'):
        manipulator.moveVerRail(-100)
    
    elif key == ord('b'):
        manipulator.grabManipulator(False)

    elif key == ord('m'):
        manipulator.grabManipulator(True)

    elif key == ord('1'):
        manipulator.moveManipulator(0, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('2'):
        manipulator.moveManipulator(10, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('3'):
        manipulator.moveManipulator(20, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('4'):
        manipulator.moveManipulator(30, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('5'):
        manipulator.moveManipulator(40, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('6'):
        manipulator.moveManipulator(50, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('7'):
        manipulator.moveManipulator(60, 0)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()
    elif key == ord('8'):
        manipulator.moveManipulator(35, 30)
        if 'moveDone' in  str(manipulator.get_data(timeout=0.5)):
            old_cords = manipulator.getCoordinates()    
    print(old_cords)

    ret, data = get_center_contour(hand_cam)
    if not ret: continue

    new_cords = (old_cords.x, old_cords.y)

    if finding_flag:
        cX, cY = data[0]
        cnt = data[1]
        result = data[-1].copy()
        file = data[-1].copy()
        area = cv2.contourArea(cnt)
        
        cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
        cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(result, f"Area: {int(area)}", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.imshow('result', result)

        new_cords = remath_cords((old_cords.x, old_cords.y), (cX, cY))
        new_cords = (int(new_cords[0]), int(new_cords[-1]))
        if not st.cube_take_limit.contains_p(Point(*new_cords)): continue

    if key == ord('s'):
        cv2.imwrite(f'additions/photos/cubs/{i}.jpg', file)
        cv2.imwrite(f'additions/photos/cubs/{i}_processed.jpg', result)
        i+=1
    

    if start_flag or timer.now()-start>=timedelta(seconds=3):
        if old_cords.x==new_cords[0] and old_cords.y==new_cords[-1]: continue
        start_flag=False
        print(new_cords)
        manipulator.moveManipulator(*new_cords)
        old_cords = manipulator.getCoordinates()
        start = timer.now()






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