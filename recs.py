import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)


cv2.namedWindow('Controls')
cv2.createTrackbar('Brightness', 'Controls', 180, 255, lambda x: None)
cv2.createTrackbar('Saturation', 'Controls', 30, 255, lambda x: None)
cv2.createTrackbar('FPS', 'Controls', 5, 100, lambda x: None)
#cv2.createTrackbar('Canny Low', 'Controls', 10, 100, lambda x: None)
#cv2.createTrackbar('Canny High', 'Controls', 30, 200, lambda x: None)

fps = 30

frame_interval = 1.0 / fps

last_frame_time = time.time()

start_time = time.time()

ret, frame = cap.read()

while True:
    # fps = cv2.getTrackbarPos('FPS', 'Controls')
    # frame_interval = 1.0 / fps
    cur_time = time.time()

    if cur_time - last_frame_time >= frame_interval:
            ret, frame = cap.read()
            if not ret:
                break


    key = cv2.waitKey(1) & 0xFF

    #ret, frame = cap.read()

    frame = cv2.flip(frame, -1)
    
    brightness = 240#cv2.getTrackbarPos('Brightness', 'Controls')
    saturation = 10#cv2.getTrackbarPos('Saturation', 'Controls')
    #canny_low = cv2.getTrackbarPos('Canny Low', 'Controls')
    #canny_high = cv2.getTrackbarPos('Canny High', 'Controls')
    
    # 1. Выделяем белый цвет в HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, brightness])
    upper_white = np.array([180, saturation, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # 2. Улучшаем маску
    kernel = np.ones((3,3), np.uint8)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)
    
    # 3. Применяем маску
    white_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    white_gray = cv2.bitwise_and(white_gray, white_gray, mask=white_mask)

    # Применяем размытие для уменьшения шума
    #blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Детектор Кэнни для обнаружения границ
    edges = cv2.Canny(white_gray, 50, 150)
    
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
    cv2.imshow('mask', white_mask)
    cv2.imshow('result', result)

    if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()