import numpy as np
from enum import StrEnum

class Color(StrEnum):
    red = 'red'
    blue = 'blue'
    yellow = 'yellow'
    white = 'white'

class Mask:
    def __init__(self, name: Color, h: tuple, s: tuple, v: tuple):
        self.name = name
        self.lower = np.array([h[0], s[0], v[0]])
        self.upper = np.array([h[-1], s[-1], v[-1]])
    
    def __str__(self):
        return self.name
    
    def contains_h(self, h):
        return self.lower[0] <= h <= self.upper[0]
    
    def contains_s(self, s):
        return self.lower[1] <= s <= self.upper[1]
    
    def contains_v(self, v):
        return self.lower[-1] <= v <= self.upper[-1]
    
    def contains_hsv(self, h, s, v):
        conditions = [
            self.contains_h(h),
            self.contains_s(s),
            self.contains_v(v)
        ]
        return all(conditions)