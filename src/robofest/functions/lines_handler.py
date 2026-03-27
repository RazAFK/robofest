import cv2
import numpy as np

from robofest.settings import masks_settings as mst
from robofest.classes.geometry_class import Point, Segment, segment_belongs_segment
from robofest.classes.limit_class import Limits

def process_frame(frame):
    if frame is None: return None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, mst.line.lower, mst.line.upper)
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    blurred = cv2.GaussianBlur(masked, (15, 15), 3)
    edges = cv2.Canny(blurred, 50, 150)
    
    return edges

def process_lines(old_lines, new_lines):
    if new_lines is not None:
        for line in new_lines:
            if type(line) is Segment:   
                x1, y1, x2, y2 = line.p1.x, line.p1.y, line.p2.x, line.p2.y
            else:
                x1, y1, x2, y2 = line[0]
            l = Segment(Point(x1, y1), Point(x2, y2))
            exist_flag = False
            for i, nl in enumerate(old_lines):
                if segment_belongs_segment(l, nl):
                    old_lines[i].update(l)
                    exist_flag = True
                if exist_flag: break
            if not(exist_flag):
                old_lines.append(l)
    return old_lines

def get_lines(edges):
    if edges is None: return None

    lines = cv2.HoughLinesP(edges, 2, np.pi/180, threshold=60, minLineLength=10, maxLineGap=20)
    
    class_lines = process_lines([], lines)

    return class_lines

def filter_lines(lines, limit: Limits):
    new_lines = []
    if lines is not None:
        for line in lines:
            if limit.contains_segment(line):
                new_lines.append(line)
    return new_lines

def filter_lines_by(lines, limit: Limits, *args: Limits.Conditions):
    new_lines = []
    if lines is not None:
        for line in lines:
            if limit.filter_segment_by(line, *args):
                new_lines.append(line)
    return new_lines

def handl_lines(frame, limit):
    edges = process_frame(frame)
    lines = get_lines(edges)
    return filter_lines(lines, limit)

def handl_lines_by(frame, limit, *args):
    edges = process_frame(frame)
    lines = get_lines(edges)
    return filter_lines_by(lines, limit, *args)