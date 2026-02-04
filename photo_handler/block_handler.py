import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)


from settings import settings as st
from photo_handler.camera_class import Camera, Flip
from photo_handler.num_handler import reader_result


from sklearn.cluster import KMeans
from collections import Counter
import cv2
import numpy as np

def get_center_contour(cam: Camera):
    '''
    return True, [(x, y), contours, frame]\n
    or\n
    return False, None
    '''
    cam.trash_frames()
    frame = cam.get_frame(Flip.hand)
    if frame is None:
        return False, None
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


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
    if len(contours)==0: return False, None
    cnt = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(cnt)
    M = cv2.moments(hull)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    return True, [(cX, cY), cnt, frame]

def get_dominant_color(image, k=3):
    pixels = image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_
    
    labels = kmeans.labels_
    label_counts = Counter(labels)
    dominant_label = label_counts.most_common(1)[0][0]
    
    return colors[dominant_label].astype(int)

# def classify_color(hsv):
#     if st.card_blue.contains_hsv(*hsv):
#         return st.Color.blue
#     if st.card_yellow.contains_hsv(*hsv):
#         return st.Color.yellow
#     if st.card_red_start.contains_hsv(*hsv) or st.card_red_end.contains_hsv(*hsv):
#         return st.Color.red
#     return None

def is_special_color(frame, cnt, color: st.Colors) -> bool:
    x, y, w, h = cv2.boundingRect(cnt)
    obj_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.drawContours(obj_mask, [cnt], -1, 255, -1)
    
    extracted_obj = cv2.bitwise_and(frame, frame, mask=obj_mask)
    crop_bgr = extracted_obj[y:y+h, x:x+w]
    
    crop_hsv = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2HSV)
    dominant_hsv = get_dominant_color(crop_hsv)
    return color.contains_hsv(*dominant_hsv)
    #return classify_color(dominant_hsv)


def get_storage_centers(cam: Camera, reader):
    cam.trash_frames()
    frame = cam.get_frame(Flip.hand)
    result = reader_result(frame, reader)
    centers = []
    for res in result:
        text, conf = res[1], round(float(res[-1]))
        if len(text)==1 and conf>0.85:
            tl, br = list(map(int, res[0][0])), list(map(int, res[0][-2]))
            x = int((abs(tl[0] - br[0]))/2) + tl[0]
            y = int((abs(tl[-1] - br[-1]))/2) + tl[-1]
            centers.append(((x, y), text, conf, frame))
    return centers

def remath_cords(old_abs: tuple[float, float], new_rel: tuple[float, float], old_rel: tuple[float, float]=(st.weight/2, st.height/2), coef: float=st.cam_coef_sp):
    '''
    old_abs: (x, y) absolute cords\n
    new_rel: (x, y) relative cords\n
    old_rel: (x, y) relative old cords highly depends by weight and height\n
    coef: santimetrs/pixels
    '''
    xA = abs(old_abs[0] - (coef*(old_rel[0]-new_rel[0])))
    yA = abs(old_abs[-1] - (coef*(old_rel[-1]-new_rel[-1])))
    return (xA, yA)