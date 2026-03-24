from robofest.settings import settings as st

from robofest.classes.camera_class import Camera, Flip, flip
from robofest.classes.limit_class import Limits
from robofest.classes.arduino_class import Arduino
from robofest.classes.pid_class import PID

from robofest.functions.lines_handler import get_lines, process_frame
from robofest.functions.eco_utilities import get_average_between, Params
from robofest.functions.drow_funcs import drow_lines, drow_lines_params

import time, cv2

def levelout_lines(cam: Camera, arduino: Arduino, target: tuple, cam_flip: Flip = Flip.default):
    
    
    target_angle = target[0]
    target_length = target[1]
    target_x = target[-1][0]
    target_y = target[-1][-1]
    
    angle_pid = PID(kp=0.005, ki=0.001, kd=0.01)
    length_pid = PID(kp=0.5, ki=0.01, kd=0.1)
    x_pid = PID(kp=0.5, ki=0.01, kd=0.1)
    y_pid = PID(kp=0.5, ki=0.01, kd=0.1)

    
    last_time = time.time()

    while True:

        frame = cam.get_frame()
        lines = get_lines(process_frame(frame))
        if lines is None:
            continue

        current_angle = get_average_between(lines, Params.angle, length=(100, 1000))
        if current_angle is None: continue

        now = time.time()
        dt = now - last_time
        if dt <= 1: continue

        rotation_speed = angle_pid.compute(target_angle, current_angle, dt)
        
        rotation_speed = max(min(rotation_speed, 0.45), -0.45)
        
        # arduino.whe.rotate(rotation_speed)
        print(rotation_speed)
        frame = drow_lines(frame, lines, (0, 0, 255))
        frame = drow_lines_params(frame, lines)
        cv2.putText(frame, f'length: {get_average_between(lines, Params.length, length=(0, 1000))}', (20, st.wheels_height-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f'angle: {get_average_between(lines, Params.angle, angle=(-90, 90))}', (20, st.wheels_height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f'cord: {get_average_between(lines, Params.position, position=((0,0), (640, 480)))}', (20, st.wheels_height-80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break

        if abs(target_angle - current_angle) < 0.5:
            break

        last_time = now


        

