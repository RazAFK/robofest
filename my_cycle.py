import cv2
import numpy as np


cap = cv2.VideoCapture(1)

while True:
    key = cv2.waitKey(1) & 0xFF

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

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Рассчитываем длину линии
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            line_thickness = 2

            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), line_thickness)

    cv2.imshow('edges', edges)
    cv2.imshow('result', result)
    cv2.imshow('masked', masked)

    if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

