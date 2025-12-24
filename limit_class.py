

class Limits:
    def __init__(self, sizes: tuple, length=(0, 1000), angle=(-90, 90), v_bounds=(0, 1), h_bounds=(0, 1)):
        '''
        length = (length_min, length_max)\n
        angle = (angle_min, angle_max)\n
        v_bounds = (v_bounds_min, v_bounds_max) equal weight*[0, 1]\n
        h_bounds = (h_bounds_min, h_bounds_max) equal height*[0, 1\n
        sizes = (height, weight)     
        '''
        self.length = length 
        self.angle = angle
        self.v_bounds = v_bounds
        self.h_bounds = h_bounds
        self.sizes = sizes

        self.length_min, self.length_max = self.length[0], self.length[-1]
        self.angle_min, self.angle_max = self.angle[0], self.angle[-1]
        self.v_bounds_min, self.v_bounds_max = self.v_bounds[0], self.v_bounds[-1]
        self.h_bounds_min, self.h_bounds_max = self.h_bounds[0], self.h_bounds[-1]
        self.height, self.weight = self.sizes[0], self.sizes[-1]

    def depends(self, s):
        length = self.length_min <= s.length <= self.length_max
        angle = self.angle_min <= s.angle <= self.angle_max
        v_bounds = (self.v_bounds_min*self.weight<= s.y1 <= self.v_bounds_max*self.weight) and (self.v_bounds_min*self.weight <= s.y2 <= self.v_bounds_max*self.weight)
        h_bounds = (self.h_bounds_min*self.height <= s.x1 <= self.h_bounds_max*self.height) and (self.h_bounds_min*self.height <= s.x2 <= self.h_bounds_max*self.height)
        return length and angle and v_bounds and h_bounds