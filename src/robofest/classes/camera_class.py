import cv2, os
from enum import StrEnum

from robofest.settings import settings as st

class Flip(StrEnum):
    wheels = 'wheels'
    hand = 'hand'
    debug = 'debug'

def flip(frame: cv2.Mat, flip: Flip):
    if frame is None: return None
    if flip==Flip.debug: return frame
    if flip==Flip.wheels: return cv2.rotate(frame, cv2.ROTATE_180)
    if flip==Flip.hand: return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

class Camera:
    def __init__(self, id):
        self.back = cv2.CAP_DSHOW
        if os.name=='posix':
            self.back = cv2.CAP_V4L2
        self.cap = cv2.VideoCapture(id, self.back)
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, st.cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, st.cap_height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret: return None
        return frame
    
    def trash_frames(self, trash_frames=st.trash_frames):
        for _ in range(trash_frames):
            self.get_frame()