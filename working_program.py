import cv2
import numpy as np
from time import sleep
from datetime import datetime
from line_class import *
from camera_class import *
import settings as st

cam = Camera(1)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    frame = cam.get_frame()
    edges = cam.process_frame_top(frame)
    lines = cam.get_lines(edges)
    lines = cam.process_lines(lines, st.central_line_limit)
    result = cam.drow_lines(frame, lines)
    cv2.imshow('result', result)

cam.cap.release()
cv2.destroyAllWindows()