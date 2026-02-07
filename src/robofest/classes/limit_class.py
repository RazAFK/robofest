from robofest.classes.geometry_class import Point, Segment

class Limits:
    def __init__(self, sizes: tuple, length=(0, 1000), angle=(-90, 90), x_bounds=(0, 1), y_bounds=(0, 1)):
        '''
        sizes = (width, height)\n
        length = (length_min, length_max)\n
        angle = (angle_min, angle_max)\n
        x_bounds = (x_min, x_max) equal width*[0, 1]\n
        y_bounds = (y_min, y_max) equal height*[0, 1\n
        '''
        self.length = length 
        self.angle = angle
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.sizes = sizes

        self.length_min, self.length_max = self.length[0], self.length[-1]
        self.angle_min, self.angle_max = self.angle[0], self.angle[-1]
        self.x_min, self.x_max = self.x_bounds[0], self.x_bounds[-1]
        self.y_min, self.y_max = self.y_bounds[0], self.y_bounds[-1]
        self.width, self.height = self.sizes[0], self.sizes[-1]
    
    def contains_point(self, p: Point):
        conditions = [
            (self.x_min*self.width <= p.x <= self.x_max*self.width),
            (self.y_min*self.height <= p.y <= self.y_max*self.height)
        ]
        return all(conditions)

    def contains_segment(self, s: Segment):
        conditions = [
            (self.length_min <= s.length <= self.length_max),
            (self.angle_min <= s.angle <= self.angle_max),
            self.contains_point(s.p1),
            self.contains_point(s.p2)
        ]
        return all(conditions)
    
    def __str__(self):
        ret = f'''
        {self.__class__.__name__}:
        a: {self.angle_min, self.angle_min}
        l: {self.length_min, self.length_max}
        x: {self.x_min, self.x_max}
        y: {self.y_min, self.y_max}
        '''
        return ret
    
    def __eq__(self, value):
        conditions = [
            self.angle_min==value.angle_min,
            self.angle_min==value.angle_min,
            self.length_min==value.length_min,
            self.length_max==value.length_max,
            self.x_min==value.x_min,
            self.x_max==value.x_max,
            self.y_min==value.y_min,
            self.y_max==value.y_max
        ]
        return all(conditions)