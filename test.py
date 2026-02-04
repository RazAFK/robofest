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
from photo_handler.num_handler import init_reader
from photo_handler.block_handler import get_storage_centers


reader = init_reader()
cam = Camera(0)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    frame = cam.get_frame(Flip.debug)
    centers = get_storage_centers(cam, reader)
    for center in centers:
        cords, text, conf, result = center
        cv2.circle(result, cords, 5, (0, 255, 0), -1)
        cv2.putText(result, f'{text}, {conf}', (cords[0] - 20, cords[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('frame', frame)
    cv2.imshow('result', result)
