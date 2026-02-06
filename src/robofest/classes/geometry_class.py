import numpy as np

from robofest.settings import settings as st

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
    
class Circle:
    def __init__(self, r, x, y):
        self.r = r
        self.a = x
        self.b = y
        self.p = Point(x, y)

    def contains_point(self, p: Point):
        return self.r**2 >= ((p.x - self.a)**2 + (p.y - self.b)**2)

class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        self.length = np.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
        self.tan = (p2.x-p1.x)/(p2.y-p1.y) if (p2.y-p1.y)!=0 else None
        self.angle = np.degrees(np.atan(self.tan)) if self.tan!=None else 90
        self.b = p1.y - self.tan*p1.x if self.tan!= None else p1.y

    def __eq__(self, value):
        return (self.p1 == value.p1) and (self.p2 == value.p2)

    def update(self, s2):
        l1 = np.sqrt((s2.p1.x - self.p1.x)**2+(s2.p1.y - self.p1.y)**2)
        l2 = np.sqrt((s2.p2.x - self.p1.x)**2+(s2.p2.y - self.p1.y)**2)
        l3 = np.sqrt((s2.p2.x - self.p2.x)**2+(s2.p2.y - self.p2.y)**2)
        l4 = np.sqrt((s2.p1.x - self.p2.x)**2+(s2.p1.y - self.p2.y)**2)
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

        self.p1 = Point(min(p1, p2).x, min(p1, p2).y)
        self.p2 = Point(max(p1, p2).x, max(p1, p2).y)

    def contains_point(self, p: Point):
        c1 = Circle(st.delta_pixels, self.p1.x, self.p1.y)
        c2 = Circle(st.delta_pixels, self.p2.x, self.p2.y)
        conditions = [
            c1.contains_point(p),
            c2.contains_point(p)
            ]
        if self.tan!=None:
            conditions.append((p.y >= (p.x*self.tan + self.b - st.delta_pixels)) and (p.y <= (p.x*self.tan + self.b + st.delta_pixels)))
            return any(conditions) 
        conditions.append(((self.p1.x - st.delta_pixels) <= p.x <= (self.x2 + st.delta_pixels)) and (((self.p1.y - st.delta_pixels) <= p.y <= (self.p2.y + st.delta_pixels))))
        return any(conditions)

def segment_belongs_segment(s1: Segment, s2: Segment):
    if (s1.angle - st.delta_angle) <= s2.angle <= (s1.angle + st.delta_angle):
        l1 = np.sqrt((s2.p1.x - s1.p1.x)**2+(s2.p1.y - s1.p1.y)**2)
        l2 = np.sqrt((s2.p2.x - s1.p1.x)**2+(s2.p2.y - s1.p1.y)**2)
        l3 = np.sqrt((s2.p2.x - s1.p2.x)**2+(s2.p2.y - s1.p2.y)**2)
        l4 = np.sqrt((s2.p1.x - s1.p2.x)**2+(s2.p1.y - s1.p2.y)**2)
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
        if min(l1, l2, l3, l4) <= st.delta_pixels:
            return True
        if s1.tan!=None and s2.tan!=None and s1.tan!=s2.tan:
            return s.contains_point(p)
    return False