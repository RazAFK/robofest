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
from arduino_code import *
from enum import StrEnum

class Flip:
    base = 'base'
    hand = 'hand'
    debug = 'debug'

class Camera:
    def __init__(self, id):
        self.back = cv2.CAP_DSHOW
        if os.name=='posix':
            self.back = cv2.CAP_V4L2
        self.cap = cv2.VideoCapture(id, self.back)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.weight = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    
    def get_frame(self, flip=Flip.base):
        ret, frame = self.cap.read()
        if not(ret): return None
        if flip==Flip.base:
            frame = cv2.flip(frame, -1)
        elif flip==Flip.hand:
            # frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        return frame
    
    def trash_frames(self):
        for _ in range(st.trash_frames):
            self.get_frame(flip=Flip.debug)
    
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
                if limit.contains(line):
                    new_lines.append(line)
        return new_lines
        
    
    def drow_lines(self, frame: cv2.Mat, lines: list[Segment], line_thickness: int = 2):
        if frame is None: return None
        result = frame.copy()
        for l in lines:
            cv2.line(result, (l.x1, l.y1), (l.x2, l.y2), (0, 0, 255), line_thickness)
        return result
    
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

def define_cam(base_cam: Camera, hand_cam: Camera):
    frame = base_cam.get_frame(Flip.base)
    if frame is not None:
        cv2.imwrite(f'cameras_check/base_cam.jpg', frame)
    frame = hand_cam.get_frame(Flip.hand)
    if frame is not None:
        cv2.imwrite(f'cameras_check/hand_cam.jpg', frame)
    answ = input('write Y/n if cams right: ')
    if answ.lower()=='y':
        return base_cam, hand_cam
    return hand_cam, base_cam