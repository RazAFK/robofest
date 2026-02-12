import cv2

from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.camera_class import flip, Flip
from robofest.functions.lines_handler import handl_lines
from robofest.functions.drow_funcs import drow_limit, drow_lines, drow_lines_angles


i = 1
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        if i!=1: i-=1
    elif key == ord('d'):
        if i!=75: i+=1
    
    frame = cv2.imread(f'C:/Users/admin/Desktop/line_photos/{i}.jpg')
    if frame is None: continue
    lines = handl_lines(frame, lst.limit_move_segmen_1)
    result = drow_lines(frame, lines, (0, 0, 255))
    result = drow_limit(result, lst.limit_move_segmen_1, (0, 255, 0))
    result = drow_lines_angles(result, lines)
    if result is not None:
        cv2.putText(result, f'{i}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow(f'result', result)
    