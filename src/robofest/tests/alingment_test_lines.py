import cv2, time

from robofest.settings import settings as st

from robofest.classes.camera_class import Camera, Flip, flip
from robofest.classes.limit_class import Limits
from robofest.classes.pid_class import PID
from robofest.classes.arduino_class import Arduino

from robofest.functions.lines_handler import process_lines, get_lines, handl_lines, process_frame, filter_lines
from robofest.functions.drow_funcs import drow_lines, drow_limit, drow_lines_params
from robofest.functions.eco_utilities import get_average_between, Params

cam = Camera(1)

def nothing(x):
    pass

cv2.namedWindow('Settings')
cv2.createTrackbar('x_min', 'Settings', 0, st.cap_width, nothing)
cv2.createTrackbar('x_max', 'Settings', st.cap_width, st.cap_width, nothing)
cv2.createTrackbar('y_min', 'Settings', 0, st.cap_height, nothing)
cv2.createTrackbar('y_max', 'Settings', st.cap_height, st.cap_height, nothing)
cv2.createTrackbar('a_min', 'Settings', 90+0, 180, nothing)
cv2.createTrackbar('a_max', 'Settings', 90+90, 180, nothing)
cv2.createTrackbar('l_min', 'Settings', 200, 1000, nothing)
cv2.createTrackbar('l_max', 'Settings', 1000, 1000, nothing)

limit = Limits(
        sizes=(st.wheels_width, st.wheels_height),
        distance=(0, 1000),
        length=(200, 1000),
        angle=(-90, 90),
        x_bounds=(0, st.wheels_width),
        y_bounds=(0, st.wheels_height)
    )

angles = []
lengths = []
positions = []

old_lines = []

frame_wait = 10
frame_counter = 0

last_time = time.time()
target_angle = 89
pid_flag = True

none_counter = 0
none_max = 5

pid = PID(kp=0.0005, ki=0.0001, kd=0.0001)

moving_flag = False

arduino = Arduino('COM4')

start_time = time.time()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        if len(angles)>0: print('angle', sum(angles)/len(angles))
        if len(lengths)>0: print('length', sum(lengths)/len(lengths))
        if len(positions)>0: print('position', (round(float(sum([x[0] for x in positions])/len(positions)),2), round(float(sum([x[-1] for x in positions])/len(positions)),2)))
        break
    if moving_flag:
        if time.time()-start_time<2:
            continue
        else:
            moving_flag = False
    frame = cam.get_frame()
    if frame is None: continue

    new_lines = get_lines(process_frame(frame))
    old_lines = process_lines(old_lines, new_lines)
    # print(new_lines)
    # print(max(new_lines, key=lambda x: x.length).length)
    # print(sum([x.length for x in new_lines])/len(new_lines))

    if frame_counter<frame_wait:
        frame_counter+=1
        continue
    else: frame_counter = 0

    x_min = cv2.getTrackbarPos('x_min', 'Settings')
    x_max = cv2.getTrackbarPos('x_max', 'Settings')
    y_min = cv2.getTrackbarPos('y_min', 'Settings')
    y_max = cv2.getTrackbarPos('y_max', 'Settings')
    a_min = cv2.getTrackbarPos('a_min', 'Settings')-90
    a_max = cv2.getTrackbarPos('a_max', 'Settings')-90
    l_min = cv2.getTrackbarPos('l_min', 'Settings')
    l_max = cv2.getTrackbarPos('l_max', 'Settings')
    limit = Limits(
        sizes=(st.wheels_width, st.wheels_height),
        distance=(0, 1000),
        length=(l_min, l_max),
        angle=(a_min, a_max),
        x_bounds=(x_min, x_max),
        y_bounds=(y_min, y_max)
    )
    
    angle = get_average_between(old_lines, Params.angle, angle=(a_min, a_max), length=(l_min, l_max))
    if angle is not None:
        angles.append(angle)
    length = get_average_between(old_lines, Params.length, angle=(a_min, a_max), length=(l_min, l_max))
    if length is not None:
        lengths.append(length)
    position = get_average_between(old_lines, Params.position, angle=(a_min, a_max), length=(l_min, l_max))
    if position is not None:
        positions.append(position)

    old_lines = filter_lines(old_lines, limit)
    
    result = drow_lines(frame, old_lines, (0, 0, 255))
    result = drow_limit(result, limit, (0, 255, 0))
    # result = drow_lines_params(result, old_lines)

    cv2.putText(result, f'length: {length}', (20, st.wheels_height-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(result, f'angle: {angle}', (20, st.wheels_height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(result, f'position: {position}', (20, st.wheels_height-80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    now = time.time()
    dt = now - last_time
    print(dt)
    if pid_flag:
        if dt>1 and not moving_flag:
            if angle is not None:
                none_counter = 0
                current_angle = angle
                
                rotation_speed = pid.compute(target_angle, current_angle, dt)
                rotation_speed = round(max(min(rotation_speed, 0.45), -0.45), 4)
                print(rotation_speed)

                if abs(target_angle - current_angle) < 0.02:
                    print('pid done at', current_angle)
                    # if current_angle==90:
                    #     arduino.whe.rotate(-0.002)
                    pid_flag = False
                
                if rotation_speed!=0 and pid_flag:
                    arduino.whe.rotate(rotation_speed)
                    moving_flag = True
                
                last_time = now
            else:
                none_counter += 1
                if none_counter>=none_max:
                    arduino.whe.rotate(-0.003)
                    moving_flag = True

    if result is not None:
        cv2.imshow(f'result', result)
    print(len(old_lines))
    old_lines = []

    cv2.imshow('frame', frame)