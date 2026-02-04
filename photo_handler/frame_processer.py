import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

import cv2
import numpy as np
from time import sleep
from datetime import datetime
from photo_handler.line_class import *
from photo_handler.limit_class import *
import settings.settings as st
from photo_handler.camera_class import *

def process_frame_after_stop(cam: Camera, limit: Limits, trashold: float=1.0, frame_counter: int = 15):
    cam.trash_frames()
    lines = []
    for _ in range(frame_counter):
        frame = cam.get_frame()
        edges = cam.process_frame_top(frame)
        lines = cam.get_lines(edges)
        lines = cam.process_lines(lines, limit)
        if len(lines)==1:
            lines.append(lines)

    if not lines:
        return None, 0
    
    groups = []# list[list[Segment, counter]]
    
    for seg in lines:
        found = False
        for i in range(len(groups)):
            if sbs(seg, groups[i][0]):
                groups[i][1] += 1
                found = True
                break
        if not found:
            groups.append([seg, 1])

    best_segment, _ = max(groups, key=lambda x: x[1])
    
    return best_segment