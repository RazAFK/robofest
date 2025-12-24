import cv2
import numpy as np
from time import sleep
from datetime import datetime
from line_class import *
from limit_class import *

class Camera:
    def __init__(self, id):
        self.cap = cv2.VideoCapture(id)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.weight = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not(ret): return None
        frame = cv2.flip(frame, -1)
        return frame
    
    def process_frame_top(self, frame):
        if frame is None: return None
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])    # Нижний порог
        upper_white = np.array([179, 30, 255]) # Верхний порог
        mask = cv2.inRange(hsv, lower_white, upper_white)
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        blurred = cv2.GaussianBlur(masked, (15, 15), 3)
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    def get_lines(self, edges):
        if edges is None: return None
        lines = cv2.HoughLinesP(edges, 2, np.pi/180, threshold=60, minLineLength=10, maxLineGap=20)
        class_lines = []
        if lines is not None:
            for line in lines:
                l = Segment(*line[0])
                exist_flag = False
                for i, nl in enumerate(class_lines):
                    if sbs(l, nl):
                        class_lines[i].update(l)
                        exist_flag = True
                    if exist_flag: break
                if not(exist_flag):
                    class_lines.append(l)
        return class_lines
    
    def process_lines(self, lines, limit: Limits):
        new_lines = []
        if lines is not None:
            for line in lines:
                if limit.depends(line):
                    new_lines.append(line)
        return new_lines
        
    
    def drow_lines(self, frame: cv2.Mat, lines: list[Segment], line_thickness=2):
        if frame is None: return None
        result = frame.copy()
        for l in lines:
            cv2.line(result, (l.x1, l.y1), (l.x2, l.y2), (0, 0, 255), line_thickness)
        return result