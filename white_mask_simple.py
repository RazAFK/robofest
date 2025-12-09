import cv2
import numpy as np

# Простейший детектор белых линий
def simple_white_line_detector():
    cap = cv2.VideoCapture(1)
    
    print("Простой детектор белых линий")
    print("Нажмите 'q' для выхода")
    print("Настройте параметры в окне 'Controls'")
    
    # Создаем окно с ползунками
    cv2.namedWindow('Controls')
    cv2.createTrackbar('Brightness', 'Controls', 180, 255, lambda x: None)
    cv2.createTrackbar('Saturation', 'Controls', 30, 255, lambda x: None)
    cv2.createTrackbar('Canny Low', 'Controls', 10, 100, lambda x: None)
    cv2.createTrackbar('Canny High', 'Controls', 30, 200, lambda x: None)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, -1)
        
        # Получаем значения с ползунков
        brightness = cv2.getTrackbarPos('Brightness', 'Controls')
        saturation = cv2.getTrackbarPos('Saturation', 'Controls')
        canny_low = cv2.getTrackbarPos('Canny Low', 'Controls')
        canny_high = cv2.getTrackbarPos('Canny High', 'Controls')
        
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
        
        # 4. Находим границы
        edges = cv2.Canny(white_gray, canny_low, canny_high)
        
        # 5. Находим линии
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30,
                               minLineLength=50, maxLineGap=20)
        
        # 6. Рисуем результат
        result = frame.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        # 7. Показываем
        cv2.imshow('Original', frame)
        cv2.imshow('White Mask', white_mask)
        cv2.imshow('Detected Lines', result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    simple_white_line_detector()