import cv2
import numpy as np

def detect_lines_of_width(frame, min_width, max_width):
    """
    Обнаруживает линии определенной ширины на изображении
    
    Args:
        frame: входное изображение
        min_width: минимальная ширина линии (в пикселях)
        max_width: максимальная ширина линии (в пикселях)
    
    Returns:
        Изображение с выделенными линиями
    """
    # Конвертируем в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Применяем пороговую обработку для выделения темных линий
    # (можете изменить метод пороговой обработки в зависимости от условий освещения)
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Морфологические операции для улучшения обнаружения линий
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Находим контуры
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Создаем копию изображения для рисования
    result = frame.copy()
    
    # Фильтруем контуры по ширине
    for contour in contours:
        # Получаем ограничивающий прямоугольник
        x, y, w, h = cv2.boundingRect(contour)
        
        # Фильтруем по ширине
        if min_width <= w <= max_width:
            # Рисуем прямоугольник вокруг линии
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Добавляем текст с информацией о ширине
            cv2.putText(result, f"Width: {w}px", (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    return result

def detect_lines_hough(frame, min_width, max_width):
    """
    Альтернативный метод: использует преобразование Хафа для обнаружения линий
    с последующей фильтрацией по ширине
    """
    # Конвертируем в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Применяем размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Детектор Кэнни для обнаружения границ
    edges = cv2.Canny(blurred, 50, 150)
    
    # Преобразование Хафа для обнаружения линий
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                           minLineLength=100, maxLineGap=10)
    
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
            if min_width <= length/10 <= max_width:  # Эмпирический коэффициент
                cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), line_thickness)
    
    return result

def main():
    # Параметры для фильтрации линий по ширине
    MIN_LINE_WIDTH = 5   # минимальная ширина линии в пикселях
    MAX_LINE_WIDTH = 50  # максимальная ширина линии в пикселях
    
    # Выбор метода детектирования
    USE_HOUGH = False  # True для метода Хафа, False для метода контуров
    
    # Открываем видеопоток с камеры
    # 0 - индекс камеры по умолчанию
    cap = cv2.VideoCapture(0)
    
    # Проверяем, открылась ли камера
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return
    
    print("Нажмите 'q' для выхода")
    print("Нажмите 'h' для переключения между методами детектирования")
    print("Нажмите '+'/'-' для увеличения/уменьшения минимальной ширины")
    print("Нажмите '*'/'/' для увеличения/уменьшения максимальной ширины")
    
    while True:
        # Считываем кадр с камеры
        ret, frame = cap.read()
        
        if not ret:
            print("Ошибка: не удалось получить кадр")
            break
        
        # Обнаруживаем линии выбранным методом
        if USE_HOUGH:
            result = detect_lines_hough(frame, MIN_LINE_WIDTH, MAX_LINE_WIDTH)
            method_name = "Hough Transform"
        else:
            result = detect_lines_of_width(frame, MIN_LINE_WIDTH, MAX_LINE_WIDTH)
            method_name = "Contour Detection"
        
        # Добавляем информационную панель
        cv2.putText(result, f"Method: {method_name}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(result, f"Min Width: {MIN_LINE_WIDTH}px", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(result, f"Max Width: {MAX_LINE_WIDTH}px", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(result, "Press 'q' to quit", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Показываем результат
        cv2.imshow('Line Width Detector', result)
        
        # Обработка нажатий клавиш
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('h'):
            USE_HOUGH = not USE_HOUGH
            print(f"Переключили метод на: {'Hough Transform' if USE_HOUGH else 'Contour Detection'}")
        elif key == ord('+'):
            MIN_LINE_WIDTH += 1
            print(f"Минимальная ширина: {MIN_LINE_WIDTH}px")
        elif key == ord('-'):
            MIN_LINE_WIDTH = max(1, MIN_LINE_WIDTH - 1)
            print(f"Минимальная ширина: {MIN_LINE_WIDTH}px")
        elif key == ord('*'):
            MAX_LINE_WIDTH += 1
            print(f"Максимальная ширина: {MAX_LINE_WIDTH}px")
        elif key == ord('/'):
            MAX_LINE_WIDTH = max(MIN_LINE_WIDTH + 1, MAX_LINE_WIDTH - 1)
            print(f"Максимальная ширина: {MAX_LINE_WIDTH}px")
    
    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()