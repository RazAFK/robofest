import math

from robofest.settings import settings as st
from robofest.functions.lighter_utilities import constrain

def increment_value(value, step, lmin, lmax):
    start_value = math.floor(value/step)*step
    end_value = math.ceil(value/step)*step
    min_value = min(start_value, end_value, key=lambda x: abs(value - x))
    value = constrain(min_value, lmin, lmax)
    steps = round(value/step, 4)
    return steps

def get_step_angle(x, y, lx=st.rail_center_offset_x, ly=st.rail_center_offset_y, step=st.rail_step, lmin=st.limit_horizontal_lenght_min, lmax=st.limit_horizontal_lenght_max, astep=st.rail_angle_step, amin=st.limit_horizontal_angle_min, amax=st.limit_horizontal_angle_max):
    opp = abs(y - ly)
    adj = abs(x - lx)
    if (x < lx) and (y <= ly):
        extra_angle = math.pi/2
    elif (x >= lx) and (y < ly):
        extra_angle = math.pi
        opp, adj = adj, opp
    elif (x <= lx) and (y > ly):
        extra_angle = 0
        opp, adj = adj, opp
    elif (x > lx) and (y >= ly):
        extra_angle = math.pi*3/2
    else:
        return increment_value(0, step, lmin, lmax), math.pi/2
    angle = math.atan(opp/adj) if adj!=0 else 0
    length = adj/math.cos(angle)
    angle += extra_angle
    steps = increment_value(length, step, lmin, lmax)
    angle = increment_value(math.degrees(angle), astep, amin, amax)
    return steps, angle, length

def get_coords(steps, angle, step=st.rail_step, lx=st.rail_center_offset_x, ly=st.rail_center_offset_y):
    hypot = steps*step
    x = abs(lx - math.sin(math.radians(angle))*hypot)
    y = abs(ly + math.cos(math.radians(angle))*hypot)
    return x, y

def increment_desired_to_real(val, step):
    return increment_value(val, step, val, val+30)*step