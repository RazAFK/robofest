import cv2
import numpy as np
from time import sleep
from datetime import datetime as timer
from datetime import timedelta

from photo_handler.line_class import *
from photo_handler.camera_class import *
#from photo_handler.num_handler import handl_num
from photo_handler.block_handler import get_center_contour, is_special_color

from connector.arduino_class import *

import settings.settings as st

wheels, manipulator = take_arduinos()

hand_cam = Camera(st.hand_cam_id)
base_cam = Camera(st.base_cam_id)
base_cam, hand_cam = define_cam(base_cam, hand_cam)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    ret, data = get_center_contour(hand_cam)
    if not ret: continue
    cX, cY = data[0]
    cnt = data[1]
    result = data[-1].copy()
    area = cv2.contourArea(cnt)
    color = is_special_color(result, cnt, st.cube_blue)
    
    cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
    cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(result, f"Area: {int(area)}, Color: {color}", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('result', result)

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