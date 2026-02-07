import cv2

from robofest.classes.reader_class import Reader
from robofest.functions.utilities import get_dominant_color, classify_color
from robofest.settings import masks_settings as mst
from robofest.settings import settings as st

def get_nums(frame, reader: Reader):
    results = []

    if frame is None:
        return results

    result = reader.result(frame)

    for res in result:
        cord=res[0]
        number=res[1]
        conf=res[2]

        padding = 5 

        x_cords = [point[0] for point in cord]
        y_cords = [point[1] for point in cord]
        
        x_min = int(max(0, min(x_cords) - padding))
        x_max = int(min(frame.shape[1], max(x_cords) + padding))
        y_min = int(max(0, min(y_cords) - padding))
        y_max = int(min(frame.shape[0], max(y_cords) + padding))

        area = (x_max-x_min)*(y_max-y_min)
        
        digit_region = frame[y_min:y_max, x_min:x_max]

        hsv_frame = cv2.cvtColor(digit_region, cv2.COLOR_BGR2HSV)
    
        dominant_hsv = get_dominant_color(hsv_frame)
        color = classify_color(dominant_hsv, [
            mst.cube_blue,
            mst.card_red_start,
            mst.card_red_end,
            mst.card_yellow
        ])
        results.append((number, color, area, cord))

    return results

def filter_nums(nums):
    if len(nums)>0:
        max_area = max(nums, key=lambda x: x[-2])
        cords = [tuple(map(int, cord)) for cord in max_area[-1]]
        return True, (list(max_area[:-1])+list(cords))
    return False, (None, None)

def is_right_num(num):
    conditions = [
        len(num[0])==1,
        num[2] > st.limit_min_area_num
    ]
    return all(conditions)

def handl_num(frame, reader: Reader):
    nums = get_nums(frame, reader)
    ret, num = filter_nums(nums)
    if ret and is_right_num(num): return nums[0]
    return None