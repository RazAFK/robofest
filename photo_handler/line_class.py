import numpy as np
import settings.settings as st
from math import ceil, floor
from datetime import datetime


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.p1 = Point(x1,y1)
        self.p2 = Point(x2,y2)
        self.length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        self.tan = (x2-x1)/(y2-y1) if (y2-y1)!=0 else None
        self.angle = np.degrees(np.atan(self.tan)) if self.tan!=None else 90
        self.b = y1 - self.tan*x1 if self.tan!= None else y1

    def __eq__(self, value):
        return (self.p1 == value.p1) and (self.p2 == value.p2)

    def update(self, s2):
        l1 = np.sqrt((s2.x1 - self.x1)**2+(s2.y1 - self.y1)**2)
        l2 = np.sqrt((s2.x2 - self.x1)**2+(s2.y2 - self.y1)**2)
        l3 = np.sqrt((s2.x2 - self.x2)**2+(s2.y2 - self.y2)**2)
        l4 = np.sqrt((s2.x1 - self.x2)**2+(s2.y1 - self.y2)**2)
        ml = max(l1, l2, l3, l4)
        if l1==ml:
            p1 = self.p1
            p2 = s2.p1
        elif l2==ml:
            p1 = self.p1
            p2 = s2.p2           
        elif l3==ml:
            p2 = s2.p2
            p1 = self.p2
        else:
            p2 = s2.p1
            p1 = self.p2

        self.x1, self.y1 = min(p1, p2).x, min(p1, p2).y
        self.x2, self.y2 = max(p1, p2).x, max(p1, p2).y
         

class Circle:
    def __init__(self, r, x, y):
        self.r = r
        self.a = x
        self.b = y
        self.p = Point(x, y)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, value):
        return (self.x == value.x) and (self.y == value.y)

    def __str__(self):
        return f'({self.x}; {self.y})'
    
    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)
    
    def depends_circle(self, c: Circle):
        return c.r**2 >= ((self.x - c.a)**2 + (self.y - c.b)**2)
    
    def depends_segment(self, s: Segment):
        if s.tan!=None:
            return self.depends_circle(Circle(st.dp, s.x1, s.y1)) or self.depends_circle(Circle(st.dp, s.x2, s.y2)) or ((self.y >= (self.x*s.tan + s.b - st.dp)) and (self.y <= (self.x*s.tan + s.b + st.dp)))
        return self.depends_circle(Circle(st.dp, s.x1, s.y1)) or self.depends_circle(Circle(st.dp, s.x2, s.y2)) or (((s.x1 - st.dp) <= self.x <= (s.x2 + st.dp)) and (((s.y1 - st.dp) <= self.y <= (s.y2 + st.dp))))

def sbs(s1: Segment, s2: Segment):
    if (s1.angle - st.da) <= s2.angle <= (s1.angle + st.da):
        l1 = np.sqrt((s2.x1 - s1.x1)**2+(s2.y1 - s1.y1)**2)
        l2 = np.sqrt((s2.x2 - s1.x1)**2+(s2.y2 - s1.y1)**2)
        l3 = np.sqrt((s2.x2 - s1.x2)**2+(s2.y2 - s1.y2)**2)
        l4 = np.sqrt((s2.x1 - s1.x2)**2+(s2.y1 - s1.y2)**2)
        ml = min(l1, l2, l3, l4)
        if l1==ml:
            p = s1.p1
            s = s2
        elif l2==ml:
            p = s1.p2
            s = s2           
        elif l3==ml:
            p = s2.p2
            s = s1
        else:
            p = s2.p1
            s = s1  

        if min(l1, l2, l3, l4) <= st.dp:
            return True
        if s1.tan!=None and s2.tan!=None and s1.tan!=s2.tan:
            return p.depends_segment(s)
    return False