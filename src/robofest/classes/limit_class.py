from __future__ import annotations

from robofest.classes.geometry_class import Point, Segment

class Limits:

    def __init__(self, sizes: tuple, distance=(0, 1000), length=(0, 1000), angle=(-90, 90), x_bounds=(0, 1), y_bounds=(0, 1)):
        '''
        sizes = (width, height)\n
        distance = (distance_min, distance_max) distance from center\n
        length = (length_min, length_max)\n
        angle = (angle_min, angle_max)\n
        x_bounds = (x_min, x_max) equal width*[0, 1]\n
        y_bounds = (y_min, y_max) equal height*[0, 1\n
        '''
        self.distance = distance
        self.length = length 
        self.angle = angle
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.sizes = sizes

        self.distance_min, self.distance_max = self.distance[0], self.distance[-1]
        self.length_min, self.length_max = self.length[0], self.length[-1]
        self.angle_min, self.angle_max = self.angle[0], self.angle[-1]
        self.x_min, self.x_max = self.x_bounds[0], self.x_bounds[-1]
        self.y_min, self.y_max = self.y_bounds[0], self.y_bounds[-1]
        self.width, self.height = self.sizes[0], self.sizes[-1]

        self.center = Point(self.width*(self.x_max-self.x_min)/2, self.height*(self.y_max-self.x_min)/2)
        
        self.conditions = self.Conditions(self)

    def contains_point(self, p: Point):
        conditions = [
            (self.x_min*self.width <= p.x <= self.x_max*self.width),
            (self.y_min*self.height <= p.y <= self.y_max*self.height)
        ]
        return all(conditions)

    class Conditions:
        def __init__(self, master: Limits):
            self.master = master

        def distance(self, s: Segment):
            return self.master.distance_min <= s.shortest_distance(self.master.center) <= self.master.distance_max
        
        def length(self, s: Segment):
            return self.master.length_min <= s.length <= self.master.length_max
        
        def angle(self, s: Segment):
            return self.master.angle_min <= s.angle <= self.master.angle_max
        
        def contains_points(self, s: Segment):
            return self.master.contains_point(s.p1) and self.master.contains_point(s.p2)
        
    
    def filter_segment_by(self, s: Segment, *args: Conditions):
        conditions = [x(s) for x in args]
        return all(conditions)
    
    def contains_segment(self, s: Segment):
        return self.filter_segment_by(s,
            self.conditions.angle,
            self.conditions.length,
            self.conditions.contains_points
        )
    
    # def contains_segment(self, s: Segment):
    #     conditions = [
    #         self.length_min <= s.length <= self.length_max,
    #         self.angle_min <= s.angle <= self.angle_max,
    #         self.contains_point(s.p1),
    #         self.contains_point(s.p2)
    #     ]
    #     return all(conditions)

    def __str__(self):
        ret = f'''
        {self.__class__.__name__}:
        sizes = {self.width, self.height},
        distance = {self.distance_min, self.distance_max},
        lenght = {self.length_min, self.length_max},
        angle = {self.angle_min, self.angle_min},
        x_bounds = {self.x_min, self.x_max},
        y_bounds = {self.y_min, self.y_max}
        '''
        return ret
    
    def __eq__(self, value: Limits):
        conditions = [
            self.distance_min==value.distance_min,
            self.distance_max==value.distance_max,
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