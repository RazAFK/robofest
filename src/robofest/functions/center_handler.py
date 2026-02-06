import cv2
import numpy as np

from robofest.settings import settings as st
from robofest.classes.reader_class import Reader

def get_center_contour(frame):
    '''
    return True, [(x, y), contours, frame]\n
    or\n
    return False, None
    '''
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]

    blurred = cv2.GaussianBlur(v_channel, (5, 5), 0)

    edged = cv2.Canny(blurred, 30, 100)

    kernel = np.ones((5, 5), np.uint8)

    dilated = cv2.dilate(edged, kernel, iterations=1)

    mask = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    kernel = np.ones((7,7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)==0: return False, None
    cnt = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(cnt)
    M = cv2.moments(hull)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    area = cv2.contourArea(cnt)
    if area < st.limit_min_area_cube:
        cnt = cv2.boundingRect(cnt)
        cX = min(cnt[0], cnt[2])+int(abs(cnt[2]-cnt[0])/2)
        cY = min(cnt[1], cnt[3])+int(abs(cnt[3]-cnt[1])/2)
    return True, ((cX, cY), cnt, frame)

def get_storage_centers(frame, reader: Reader):
    result = reader.result(frame, reader)
    centers = []
    for res in result:
        text, conf = res[1], round(float(res[-1]))
        if len(text)==1 and conf>0.85:
            tl, br = list(map(int, res[0][0])), list(map(int, res[0][-2]))
            x = int((abs(tl[0] - br[0]))/2) + tl[0]
            y = int((abs(tl[-1] - br[-1]))/2) + tl[-1]
            centers.append(((x, y), text, conf, frame))
    return centers