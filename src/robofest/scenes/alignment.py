from robofest.settings import settings as st

from robofest.classes.camera_class import Camera, Flip, flip
from robofest.classes.limit_class import Limits
from robofest.classes.arduino_class import Arduino
from robofest.classes.pid_class import PID

from robofest.functions.lines_handler import get_lines, process_frame, handl_lines, process_lines, filter_lines
from robofest.functions.eco_utilities import get_average_between, Params
from robofest.functions.drow_funcs import drow_lines, drow_lines_params

import time, cv2

def levelout_angle(cam: Camera, arduino: Arduino, target_angle: float, limit: Limits, pid: PID, cam_flip: Flip = Flip.default):
    
    last_time = time.time()

    old_lines = []

    frame_counter = 0

    none_counter = 0

    moving_flag = False
    last_time = time.time()

    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if moving_flag:
            data = arduino.get_data()
            if data is not None and  data.check_pref(st.Prefixes.move_done):
                moving_flag = False
                time.sleep(0.5)
            else:
                continue

        frame = flip(cam.get_frame(), cam_flip)
        
        new_lines = get_lines(process_frame(frame))
        old_lines = process_lines(old_lines, new_lines)

        if frame_counter < 10:
            frame_counter+=1
            continue
        else: frame_counter = 0
        
        old_lines = filter_lines(old_lines, limit)
        
        current_angle = get_average_between(old_lines, Params.angle, length=(limit.length_min, limit.length_max), angle=(limit.angle_min, limit.angle_max))
        
        result = drow_lines(frame, old_lines, (0, 0, 255))
        cv2.putText(result, f'angle: {current_angle}', (20, st.wheels_height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('res', result)

        now_time = time.time()
        dt = now_time-last_time
        if dt>1 and not moving_flag:
            if current_angle is None:
                none_counter += 1
                if none_counter>=5:
                    arduino.whe.rotate(-0.0005)
                    moving_flag = True
            else:
                none_counter = 0
                rotation_speed = pid.compute(target_angle, current_angle, dt)
                rotation_speed = round(max(min(rotation_speed, 0.45), -0.45), 4)
                if abs(target_angle - current_angle) < pid.admission:
                    print(current_angle)
                    return True
                if rotation_speed != 0:
                    arduino.whe.rotate(rotation_speed)
                    moving_flag = True
                last_time = now_time
        old_lines = []
