from sklearn.cluster import KMeans
from collections import Counter

from robofest.classes.color_class import Mask
from robofest.settings import settings as st

def constrain(x, start, end):
    return x if start<=x<=end else start if x<start else end

def get_dominant_color(image, k=3):
    pixels = image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_
    
    labels = kmeans.labels_
    label_counts = Counter(labels)
    dominant_label = label_counts.most_common(1)[0][0]
    
    return colors[dominant_label].astype(int)

def classify_color(hsv, masks: list[Mask]):
    for mask in masks:
        if mask.contains_hsv(*hsv):
            return mask.name
    return None

def remath_cords(old_abs: tuple[float, float], new_rel: tuple[float, float], old_rel: tuple[float, float], coef: float=st.cam_coef_san_pix):
    '''
    old_abs: (x, y) absolute cords\n
    new_rel: (x, y) relative cords\n
    old_rel: (x, y) relative old cords highly depends by weight and height\n
    coef: santimetrs/pixels
    '''
    xA = abs(old_abs[0] - (coef*(old_rel[0]-new_rel[0])))
    yA = abs(old_abs[-1] - (coef*(old_rel[-1]-new_rel[-1])))
    return (xA, yA)