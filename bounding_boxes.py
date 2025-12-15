import cv2
import numpy as np

class StraightLineFilter:
    def __init__(self, min_width=5, max_width=30, min_length=50):
        self.min_width = min_width
        self.max_width = max_width
        self.min_length = min_length
        
    def process_frame(self, frame):
        # Преобразование в серый
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Бинаризация (для светлых линий на темном фоне)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Или для темных линий на светлом фоне:
        # _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        
        # Морфологические операции
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # Поиск контуров
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Фильтрация контуров
        filtered_lines = self.filter_contours(contours)
        
        # Визуализация
        result = frame.copy()
        binary_display = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        # Рисуем ВСЕ контуры (серым)
        for contour in contours:
            cv2.drawContours(binary_display, [contour], -1, (100, 100, 100), 1)
        
        # Рисуем ОТФИЛЬТРОВАННЫЕ линии (цветом)
        for line_info in filtered_lines:
            contour = line_info['contour']
            x, y, w, h = line_info['bbox']
            
            # Bounding box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Контур
            cv2.drawContours(result, [contour], -1, (0, 0, 255), 2)
            cv2.drawContours(binary_display, [contour], -1, (0, 0, 255), 2)
            
            # Информация
            info = f"W:{line_info['width']:.0f} L:{line_info['length']:.0f}"
            cv2.putText(result, info, (x, y-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return result, binary_display, filtered_lines
    
    def filter_contours(self, contours):
        """Основная фильтрация контуров"""
        lines = []
        
        for contour in contours:
            # 1. Пропускаем слишком маленькие
            area = cv2.contourArea(contour)
            if area < 50:
                continue
            
            # 2. Получаем bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # 3. Определяем ориентацию и размеры
            is_horizontal = w > h
            length = max(w, h)
            width = min(w, h)
            
            # 4. Фильтр по длине
            if length < self.min_length:
                continue
            
            # 5. Фильтр по ширине
            if width < self.min_width or width > self.max_width:
                continue
            
            # 6. Проверка соотношения сторон (линия должна быть длинной и узкой)
            aspect_ratio = length / max(width, 1)
            if aspect_ratio < 3:  # Минимум 3:1
                continue
            
            # 7. Проверка на "прямоту" через минимальный ограничивающий прямоугольник
            rect = cv2.minAreaRect(contour)
            (_, _), (rect_w, rect_h), angle = rect
            
            # Отношение сторон rotated rect должно быть большим
            rotated_aspect = max(rect_w, rect_h) / max(min(rect_w, rect_h), 1)
            if rotated_aspect < 2.5:
                continue
            
            # 8. Проверка формы через аппроксимацию
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Прямая линия должна иметь мало вершин
            if len(approx) > 6:
                continue
            
            # 9. Проверка компактности (линия должна быть вытянутой)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            if circularity > 0.2:  # Близко к кругу - не линия
                continue
            
            # 10. Сохраняем отфильтрованную линию
            lines.append({
                'contour': contour,
                'bbox': (x, y, w, h),
                'length': length,
                'width': width,
                'aspect_ratio': aspect_ratio,
                'area': area,
                'rotated_rect': rect,
                'approx_points': len(approx),
                'circularity': circularity
            })
        
        return lines

# Основной код
def main():
    # Параметры фильтрации
    MIN_WIDTH = 3    # Минимальная ширина линии (пиксели)
    MAX_WIDTH = 30   # Максимальная ширина линии
    MIN_LENGTH = 50  # Минимальная длина линии
    
    filter = StraightLineFilter(MIN_WIDTH, MAX_WIDTH, MIN_LENGTH)
    cap = cv2.VideoCapture(1)
    
    print("Детектор прямых линий с фильтрацией по ширине")
    print(f"Параметры: ширина {MIN_WIDTH}-{MAX_WIDTH}px, длина от {MIN_LENGTH}px")
    print("Нажмите 'q' для выхода")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, -1)
        
        # Обработка кадра
        result, binary_display, lines = filter.process_frame(frame)
        
        # Статистика
        cv2.putText(result, f"Lines found: {len(lines)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Отображение
        cv2.imshow('Filtered Lines', result)
        cv2.imshow('Binary + Contours', binary_display)
        
        # Показать информацию о найденных линиях
        if lines:
            print(f"\nНайдено линий: {len(lines)}")
            for i, line in enumerate(lines):
                print(f"  Линия {i+1}: {line['width']:.0f}px x {line['length']:.0f}px, " +
                      f"соотношение {line['aspect_ratio']:.1f}:1")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()