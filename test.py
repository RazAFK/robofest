from photo_handler.camera_class import *

import os
from settings import settings as st

import cv2

import warnings, logging
warnings.filterwarnings("ignore", message=".*pin_memory.*")
logging.getLogger('easyocr').setLevel(logging.ERROR)

import easyocr
from sklearn.cluster import KMeans
from collections import Counter
from photo_handler.camera_class import Camera, Flip
# from photo_handler.num_handler import init_reader
from photo_handler.block_handler import get_center_contour

i = 1

frame = cv2.imread(f'additions/photos/cubs/{i}.jpg')

ret, result = get_center_contour(frame)
p = Point(*result[0])
contour = result[1]
rect = cv2.boundingRect(contour)
frame = result[-1]
result = frame.copy()
while True:
    frame = cv2.imread(f'additions/photos/cubs/{i}.jpg')
    ret, result = get_center_contour(frame)
    p = Point(*result[0])
    contour = result[1]
    rect = cv2.boundingRect(contour)
    frame = result[-1]
    result = frame.copy()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        i+=1
    elif key == ord('a'):
        i-=1
    # cv2.imshow('frame', frame)
    # for cont in contour:
    cv2.drawContours(result, [contour], -1, (0, 255, 0), 2)
    cv2.circle(result, (p.x, p.y), 4, (0, 255, 0), -1)
    cv2.imshow(f'{i}', result)

cv2.destroyAllWindows()