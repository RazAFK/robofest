import cv2

from robofest.classes.geometry_class import Segment
from robofest.classes.limit_class import Limits

def drow_lines(frame: cv2.Mat, lines: list[Segment], color = (0, 255, 0), line_thickness: int = 2):
    if frame is None: return None
    result = frame.copy()
    for l in lines:
        cv2.line(result, (l.p1.x, l.p1.y), (l.p2.x, l.p2.y), color, line_thickness)
    return result

def drow_lines_angles(frame: cv2.Mat, lines: list[Segment], color = (255, 0, 0), line_thickness: int = 2):
    if frame is None: return None
    result = frame.copy()
    for l in lines:
        cv2.putText(result, f'{round(l.angle, 2)}', (l.p1.x, l.p1.y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, line_thickness)
    return result

def drow_limit(frame: cv2.Mat, limit: Limits, color = (0, 0, 255), line_thickness: int = 2):
    if frame is None: return None
    result = frame.copy()
    #||
    cv2.line(result, (int(limit.x_bounds[0]*limit.width), 0), (int(limit.x_bounds[0]*limit.width), limit.height), color, line_thickness)
    cv2.line(result, (int(limit.x_bounds[-1]*limit.width), 0), (int(limit.x_bounds[-1]*limit.width),limit.height), color, line_thickness)
    #=
    cv2.line(result, (0, int(limit.y_bounds[0]*limit.height)), (limit.width, int(limit.y_bounds[0]*limit.height)), color, line_thickness)
    cv2.line(result, (0, int(limit.y_bounds[-1]*limit.height)), (limit.width, int(limit.y_bounds[-1]*limit.height)), color, line_thickness)

    cv2.lint(result, (0, 0), ())
    return result