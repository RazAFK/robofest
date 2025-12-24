import cv2
import numpy as np
from time import sleep
from datetime import datetime
from line_class import *




cap = cv2.VideoCapture(1)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
weight = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print(height, weight)
flag = True
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])    # Нижний порог
    upper_white = np.array([179, 30, 255]) # Верхний порог

    # 4. Создание маски
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # 5. Применение маски к оригиналу (опционально)
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Применяем размытие для уменьшения шума
    blurred = cv2.GaussianBlur(masked, (15, 15), 3)
    
    # Детектор Кэнни для обнаружения границ
    edges = cv2.Canny(blurred, 50, 150)
    
    # Преобразование Хафа для обнаружения линий
    lines = cv2.HoughLinesP(edges, 2, np.pi/180, threshold=60, minLineLength=100, maxLineGap=20)
    
    result = frame.copy()

    new_lines = []

    if lines is not None:
        for line in lines:
            #x1, y1, x2, y2 = line[0]
            l = Segment(*line[0])
            exist_flag = False
            for i, nl in enumerate(new_lines):
                if sbs(l, nl):
                    new_lines[i].update(l)
                    exist_flag = True
                if exist_flag: break
            
            if not(exist_flag):
                new_lines.append(l)

            line_thickness = 2
    if new_lines is not None:
        #cv2.line(result, (int(weight*0.4), 0), (int(weight*0.4), int(height)), (0, 255, 0), line_thickness)
        #cv2.line(result, (int(weight*0.6), 0), (int(weight*0.6), int(height)), (0, 255, 0), line_thickness)
        for l in new_lines:
            if l.length>200:# and (weight*0.4 <= l.x1 <= weight*0.6) and (weight*0.4 <= l.x2 <= weight*0.6):
                cv2.line(result, (l.x1, l.y1), (l.x2, l.y2), (0, 0, 255), line_thickness)
                print(l.angle, l.length)

    # cv2.imshow('edges', edges)
    # cv2.imshow('masked', masked)
    cv2.imshow('result', result)

    

cap.release()
cv2.destroyAllWindows()

