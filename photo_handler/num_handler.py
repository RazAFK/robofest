import easyocr
import cv2, os
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

print('loaded')

vc = cv2.VideoCapture(0, cv2.CAP_DSHOW) #, cv2.CAP_DSHOW cv2.CAP_V4L2 cv2.CAP_FFMPEG
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640); #1280 1600
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480); #720 1200

cur_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(cur_dir, 'model')

reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_path)

def classify_color(hsv_color):
    """
    Классифицирует цвет как красный, синий или желтый на основе HSV значений
    """
    h, s, v = hsv_color
    
    # Красный цвет (учет того, что красный может быть в начале и конце диапазона Hue)
    if (h >= 170) and s > 50 and v > 100:
        return "Красный"
    
    # Желтый цвет (диапазон примерно 20-40)
    elif h <= 20 and s > 50 and v > 50:
        return "Желтый"
    
    # Синий цвет (диапазон примерно 90-130)
    elif 90 <= h <= 130 and s > 50 and v > 50:
        return "Синий"
    
    # Если цвет не соответствует четко заданным диапазонам
    else:
        return "Не определен"
    
def get_dominant_color(image, k=3):
    """
    Определяет доминирующий цвет в изображении с помощью KMeans
    """
    # Преобразуем изображение в массив пикселей
    pixels = image.reshape(-1, 3)
    
    # Применяем KMeans для кластеризации цветов
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    # Получаем цвета центроидов
    colors = kmeans.cluster_centers_
    
    # Определяем наиболее распространенный кластер
    labels = kmeans.labels_
    label_counts = Counter(labels)
    dominant_label = label_counts.most_common(1)[0][0]
    
    return colors[dominant_label].astype(int)

while True:
    rval, frame = vc.read()
    
    result = reader.readtext(frame, allowlist='12345')
    for res in result:
        coord=res[0]
        text=res[1]
        conf=res[2]
        #print(text, conf)

        padding = 5 

        x_coords = [point[0] for point in coord]
        y_coords = [point[1] for point in coord]
        
        x_min = int(max(0, min(x_coords) - padding))
        x_max = int(min(frame.shape[1], max(x_coords) + padding))
        y_min = int(max(0, min(y_coords) - padding))
        y_max = int(min(frame.shape[0], max(y_coords) + padding))
        
        # Вырезание области
        digit_region = frame[y_min:y_max, x_min:x_max]

        # Конвертируем BGR в HSV
        hsv_frame = cv2.cvtColor(digit_region, cv2.COLOR_BGR2HSV)
    
        # Получаем доминирующий цвет в HSV
        dominant_hsv = get_dominant_color(hsv_frame)
        #print( dominant_hsv )
        print ( text, conf, classify_color(dominant_hsv) )

        '''
        # Создаем прямоугольник с доминирующим цветом
        color_rect = np.zeros((50, 50, 3), dtype=np.uint8)
        
        # Конвертируем HSV обратно в BGR для отображения
        hsv_color = np.uint8([[dominant_hsv]])
        bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
        color_rect[:] = bgr_color
        
        # Вставляем прямоугольник в основной кадр
        digit_region[10:60, 10:60] = color_rect
        
        # Отображаем кадр
        cv2.imshow('Определение цвета', digit_region)                      
        
        #cv2.imshow('Определение цвета', digit_region)            
        # Обработка клавиш
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        '''        
          


