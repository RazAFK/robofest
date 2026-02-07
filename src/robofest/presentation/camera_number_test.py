import cv2

from robofest.classes.camera_class import *
from robofest.classes.reader_class import Reader

from robofest.functions.num_handler import handl_num


cam = Camera(0)
reader = Reader()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    frame = cam.get_frame()
    frame = flip(frame, Flip.wheels)
    result = handl_num(frame, reader)
    result_frame = frame.copy()
    if result is not None:
        print(result[0], result[1])
        cv2.putText(result_frame, str(result[0])+str(result[1]), tuple(map(int, result[-1][0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(result_frame, tuple(map(int, result[-1][0])), tuple(map(int, result[-1][-2])), (0, 255, 0), 3)
        cv2.imshow('result', result_frame)
    cv2.imshow('frame', frame)