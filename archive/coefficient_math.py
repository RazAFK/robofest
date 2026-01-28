import cv2
import numpy as np
from settings import settings as st
from photo_handler.camera_class import Camera

points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # x и y — это координаты пикселя
        print(x, y)
        points.append((x, y))


# blue = cv2.imread('additions/photos/blue.jpg')
# red = cv2.imread('additions/photos/red/6.jpg')
# yellow = cv2.imread('additions/photos/yellow.jpg')
# white = cv2.imread('additions/photos/white.jpg')

# frame = white
paper = cv2.imread('additions/photos/paper/14.jpg')
paper = cv2.rotate(paper, cv2.ROTATE_90_CLOCKWISE)
cv2.namedWindow('result')
cv2.setMouseCallback('result', click_event)

while True:

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    for p in points:
        cv2.circle(paper, p, 1, (0, 0, 255), -1)
    if len(points)>=2:
        p1 = points[0]
        p2 = points[1]
        print(((p2[0]-p1[0])**2 + (p2[1]-p2[1])**2)**0.5)
        cv2.line(paper, p1, p2, (0, 255, 0))
    cv2.imshow('result', paper)


cv2.destroyAllWindows()