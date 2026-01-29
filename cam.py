import cv2
import numpy as np
from settings import settings as st
from photo_handler.camera_class import Camera, Flip

cam = Camera(0)

frame = cam.get_frame(Flip.debug)
flip = 0

while True:
    
    frame = cam.get_frame(Flip.debug)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    if key == ord('1') or flip==1:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        flip=1
    if key == ord('2') or flip==2:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip=2
    if key == ord('3') or flip==3:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip=3
    if key == ord('4') or flip==4:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        flip=4
    if key == ord('5') or flip==5:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip=5
    if key == ord('0'):
        flip=0

    cv2.imshow('frame', frame)


cam.cap.release()
cv2.destroyAllWindows()