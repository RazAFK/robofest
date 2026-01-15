import cv2
import numpy as np
from time import sleep
from datetime import datetime
from photo_handler.line_class import *
from photo_handler.camera_class import *
import settings.settings as st

cam = Camera(0)

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

segment, percent = process_frame_after_stop(cam, Limits(sizes=(st.weight, st.height), v_bounds=(0.4, 0.6), angle=(-10, 10)))

frame = cv2.flip(cam.get_frame(), -1)
res = cam.process_frame_top(frame)
result = cam.drow_lines(frame, [segment]) if segment is not None else frame
print(percent)
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    cv2.imshow('res', res)
    cv2.imshow('result', result)

cam.cap.release()
cv2.destroyAllWindows()