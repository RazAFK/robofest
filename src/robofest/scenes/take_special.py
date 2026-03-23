from robofest.settings import settings as st

from robofest.classes.camera_class import Camera, Flip, flip
from robofest.classes.reader_class import Reader

from robofest.functions.num_handler import handl_num

from datetime import datetime

def take_special(cam: Camera, reader: Reader):
    taken_results = {}
    start_time = datetime.now()
    while datetime.now()-start_time <= st.wait_card:
        frame = cam.get_frame()
        frame = flip(frame, Flip.wheels)
        card = handl_num(frame, reader)
        if not card is None:
            if card not in taken_results:
                taken_results[card] = 1
            else:
                taken_results[card] += 1
    if len(taken_results)==0:
        return (None, None)
    return max(taken_results.keys(), key=lambda x: taken_results[x])