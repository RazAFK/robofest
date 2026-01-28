import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

from settings import settings as st

import cv2

import warnings, logging
warnings.filterwarnings("ignore", message=".*pin_memory.*")
logging.getLogger('easyocr').setLevel(logging.ERROR)

import easyocr
from sklearn.cluster import KMeans
from collections import Counter
from photo_handler.camera_class import Camera, Flip



cur_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(cur_dir, 'model')
os.makedirs(model_path, exist_ok=True)

reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_path)

def classify_color(hsv):
    if st.card_blue.contains_hsv(*hsv):
        return st.Color.blue
    if st.card_yellow.contains_hsv(*hsv):
        return st.Color.yellow
    if st.card_red_start.contains_hsv(*hsv) or st.card_red_end.contains_hsv(*hsv):
        return st.Color.red
    return None

def get_dominant_color(image, k=3):
    pixels = image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_
    
    labels = kmeans.labels_
    label_counts = Counter(labels)
    dominant_label = label_counts.most_common(1)[0][0]
    
    return colors[dominant_label].astype(int)

def any_dict(dic, val):
    bool_arr = []
    for key, value in enumerate(dic):
        if value==val:
            bool_arr.append(1)
            k = key
    return k, any(bool_arr)

def max_dict(dic):
    result = [1, 0]
    for key, val in enumerate(dic):
        if val>result[-1]:
            result = [key, val]
    return result[0], result[-1]

def handl_num(cam: Camera):
    cam.trash_frames()

    frame = cam.get_frame(Flip.base)
    text = 0
    color = None

    if frame is None:
        return text, color

    result = reader.readtext(frame, allowlist='12345', )

    for res in result:
        coord=res[0]
        text=res[1]
        conf=res[2]

        padding = 5 

        x_coords = [point[0] for point in coord]
        y_coords = [point[1] for point in coord]
        
        x_min = int(max(0, min(x_coords) - padding))
        x_max = int(min(frame.shape[1], max(x_coords) + padding))
        y_min = int(max(0, min(y_coords) - padding))
        y_max = int(min(frame.shape[0], max(y_coords) + padding))
        
        digit_region = frame[y_min:y_max, x_min:x_max]

        hsv_frame = cv2.cvtColor(digit_region, cv2.COLOR_BGR2HSV)
    
        dominant_hsv = get_dominant_color(hsv_frame)
        color = classify_color(dominant_hsv)

    return text, color