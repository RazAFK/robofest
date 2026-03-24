from robofest.classes.geometry_class import Segment

from enum import StrEnum

class Params(StrEnum):
    length = 'length'
    angle = 'angle'
    position = 'position'

def get_param(line: Segment, param: Params):
    if param == Params.length:
        return line.length
    if param == Params.angle:
        return line.angle
    if param == Params.position:
        return (min(line.p1.x, line.p2.x) + abs(line.p1.x - line.p2.x), min(line.p1.y, line.p2.y) + abs(line.p1.y - line.p2.y))

def check_param(line: Segment, param: Params, bounds: tuple):
    if param == Params.position:
        return bounds[0][0] <= get_param(line, param)[0] <= bounds[-1][0] and bounds[0][-1] <= get_param(line, param)[-1] <= bounds[-1][-1]
    return bounds[0] <= get_param(line, param) <= bounds[-1]

def get_average_between(lines: list[Segment], ret: Params, **params):
    filtered_lines = []
    for line in lines:
        if all([check_param(line, param, params[param]) for param in params.keys()]):
            filtered_lines.append(get_param(line, ret))
    if len(filtered_lines)==0:
        return None
    if ret == Params.position:
        return (round(float(sum([x[0] for x in filtered_lines])/len(filtered_lines)),2), round(float(sum([x[-1] for x in filtered_lines])/len(filtered_lines)),2))
    return round(sum(filtered_lines)/len(filtered_lines), 2)