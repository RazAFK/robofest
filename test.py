import cv2
import numpy as np
from settings import settings as st
from photo_handler.camera_class import Camera

# # 1. Загрузка изображения и перевод в HSV
# img = cv2.imread('your_image.jpg')
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # 2. Определяем диапазон ФОНА (например, зеленый фон)
# lower_bg = np.array([35, 50, 50])
# upper_bg = np.array([85, 255, 255])

# # Создаем маску фона
# bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)

# # 3. ИНВЕРСИЯ: теперь объекты (кубики) стали БЕЛЫМИ (255)
# # Все, что НЕ фон, станет объектом поиска
# inv_mask = cv2.bitwise_not(bg_mask)

# # (Опционально) Убираем шум: "закрываем" дырки и убираем точки
# kernel = np.ones((5,5), np.uint8)
# inv_mask = cv2.morphologyEx(inv_mask, cv2.MORPH_OPEN, kernel)

# # 4. Поиск контуров черных областей (которые теперь белые на inv_mask)
# contours, _ = cv2.findContours(inv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# for cnt in contours:
#     area = cv2.contourArea(cnt)
    
#     # Фильтр по минимальной площади, чтобы не ловить мусор
#     if area > 500:
#         # 5. Вычисление центра масс (моменты)
#         M = cv2.moments(cnt)
#         if M["m00"] != 0:
#             cX = int(M["m10"] / M["m00"])
#             cY = int(M["m01"] / M["m00"])
            
#             # Рисуем результат
#             cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
#             cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
#             cv2.putText(img, f"Area: {int(area)}", (cX - 20, cY - 20),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# cv2.imshow("Result", img)
# cv2.imshow("Mask (Objects)", inv_mask)
# cv2.waitKey(0)

def nothing(x):
    pass

cv2.namedWindow('Settings')

cv2.createTrackbar('hi', 'Settings', st.background.lower[0], 179, nothing)
cv2.createTrackbar('ha', 'Settings', st.background.upper[0], 179, nothing)

cv2.createTrackbar('si', 'Settings', st.background.lower[1], 255, nothing)
cv2.createTrackbar('sa', 'Settings', st.background.upper[1], 255, nothing)

cv2.createTrackbar('vi', 'Settings', st.background.lower[-1], 255, nothing)
cv2.createTrackbar('va', 'Settings', st.background.upper[-1], 255, nothing)


blue = cv2.imread('additions/photos/blue.jpg')
red = cv2.imread('additions/photos/red/6.jpg')
yellow = cv2.imread('additions/photos/yellow.jpg')
white = cv2.imread('additions/photos/white.jpg')

frame = white

# cam = Camera(0)

# frame = cam.get_frame()

while True:

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
            break
    if key == ord('1'):
        frame = white
    if key == ord('2'):
        frame = yellow
    if key == ord('3'):
        frame = blue
    if key == ord('4'):
        frame = red
    if key == 13: # Enter
        # Сбрасываем минимумы в 0, максимумы в 255 (или свои значения)
        cv2.setTrackbarPos('hi', 'Settings', st.background.lower[0])
        cv2.setTrackbarPos('si', 'Settings', st.background.lower[1])
        cv2.setTrackbarPos('vi', 'Settings', st.background.lower[-1])
        cv2.setTrackbarPos('ha', 'Settings', st.background.upper[0])
        cv2.setTrackbarPos('sa', 'Settings', st.background.upper[1])
        cv2.setTrackbarPos('va', 'Settings', st.background.upper[-1])
    
    hi = cv2.getTrackbarPos('hi', 'Settings')
    si = cv2.getTrackbarPos('si', 'Settings')
    vi = cv2.getTrackbarPos('vi', 'Settings')
    ha = cv2.getTrackbarPos('ha', 'Settings')
    sa = cv2.getTrackbarPos('sa', 'Settings')
    va = cv2.getTrackbarPos('va', 'Settings')

    # frame = cam.get_frame()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask = cv2.inRange(hsv, np.array([hi, si, vi]), np.array([ha, sa, va]))
    # mask = cv2.bitwise_not(mask)
    # kernel = np.ones((5,5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)

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
    if len(contours)==0: continue
    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    img = frame.copy()

    hull = cv2.convexHull(cnt)
    M = cv2.moments(hull)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # Рисуем результат
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
        cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, f"Area: {int(area)}", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    #cv2.imshow('frame', frame)
    cv2.imshow('result', img)
    cv2.imshow('mask', mask)


# cam.cap.release()
cv2.destroyAllWindows()