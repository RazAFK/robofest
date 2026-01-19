import cv2
import os
import numpy as np
import easyocr
import platform

# Определяем систему
IS_LINUX = platform.system() == "Linux"
BACKEND = cv2.CAP_V4L2 if IS_LINUX else cv2.CAP_DSHOW

# Инициализация
vc = cv2.VideoCapture(0, BACKEND)
# На Raspberry Pi 4 лучше использовать 320x240 для скорости
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cur_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(cur_dir, 'model')
os.makedirs(model_path, exist_ok=True)

# Загружаем OCR (модель заберет около 150-300МБ ОЗУ)
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_path)

def classify_color(hsv):
    h, s, v = hsv
    if s < 50 or v < 50: return "Не определен"
    # Красный (с учетом разрыва шкалы Hue)
    if h < 10 or h > 165: return "Красный"
    # Желтый (стандарт 25-35)
    if 20 <= h <= 45: return "Желтый"
    # Синий (стандарт 100-120)
    if 90 <= h <= 135: return "Синий"
    return "Не определен"

while True:
    ret, frame = vc.read()
    if not ret:
        print("Ошибка камеры. Переподключение...")
        vc = cv2.VideoCapture(0, BACKEND)
        continue

    # Быстрый поиск цветового пятна, чтобы не гонять OCR вхолостую
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Ищем любые насыщенные цвета
    mask = cv2.inRange(hsv, np.array([0, 70, 70]), np.array([180, 255, 255]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 1500: # Порог размера карточки
            x, y, w, h = cv2.boundingRect(cnt)
            roi = frame[y:y+h, x:x+w]
            
            # OCR только на области карточки
            res = reader.readtext(roi, allowlist='12345', detail=0)
            
            if res:
                # Берем средний цвет в ROI вместо KMeans
                avg_hsv = cv2.mean(cv2.cvtColor(roi, cv2.COLOR_BGR2HSV))[:3]
                color = classify_color(avg_hsv)
                print(f"Обнаружено: {color} {res[0]}")

    cv2.imshow('RPi4 Card Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

vc.release()
cv2.destroyAllWindows()
