import datetime

class PID:
    def __init__(self, kp, ki, kd, admission):
        self.kp = kp
        
        self.ki = ki
        self.kd = kd
        self.admission = admission
        
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.prev_error = error
        return output
    
