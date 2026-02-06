import cv2

from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.camera_class import *
from robofest.classes.reader_class import Reader

from robofest.functions.num_handler import handl_num
from robofest.functions.lines_handler import handl_lines
from robofest.functions.drow_funcs import drow_lines, drow_limit

cam = Camera(0)
reader = Reader()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    frame = cam.get_frame()
    if frame is None: continue
    lines = handl_lines(frame, lst.limit_move_segmen_1)
    result = drow_lines(frame, lines)
    result = drow_limit(result, lst.limit_move_segmen_1)
    if result is not None:
        cv2.imshow('result', result)
    cv2.imshow('frame', frame)