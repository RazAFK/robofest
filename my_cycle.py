import threading
import cv2
import numpy as np
import time


cap = cv2.VideoCapture(1)

while True:
    key = cv2.waitKey(1) & 0xFF

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Применяем размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (11, 11), 3)
    
    # Детектор Кэнни для обнаружения границ
    edges = cv2.Canny(blurred, 50, 150)
    
    # Преобразование Хафа для обнаружения линий
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                           minLineLength=100, maxLineGap=15)
    
    result = frame.copy()

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Рассчитываем длину линии
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Для Хафа ширина оценивается косвенно через толщину линии
            # Можно регулировать толщину рисования в зависимости от желаемой ширины
            line_thickness = 2
            
            # Фильтруем линии по длине (как приблизительный аналог ширины)
            #if min_width <= length/10 <= max_width:  # Эмпирический коэффициент
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), line_thickness)

    cv2.imshow('edges', edges)
    cv2.imshow('blurred', blurred)
    cv2.imshow('result', result)

    if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

