from robofest.classes.limit_class import Limits
from robofest.settings import settings as st


limit_grab_cube = Limits(
    sizes = (st.arm_width, st.arm_height),
    x_bounds = (0.5-(st.cam_coef_pix_san*st.delta_grab_x/st.arm_width),
        0.5+(st.cam_coef_pix_san*st.delta_grab_x/st.arm_width)),
    y_bounds = (0.5-(st.cam_coef_pix_san*st.delta_grab_y/st.arm_height),
        0.5+(st.cam_coef_pix_san*st.delta_grab_y/st.arm_height)))


limit_move_segmen_1 = Limits((st.wheels_width, st.wheels_height), length=(200, 1000), angle=(-50, -40))

limit_first_alignment = Limits((st.wheels_width, st.wheels_height),
    distance = (0, 500),
    length = (200, 500),
    angle = (-90, -90),
    x_bounds = (0.15, 0.85),
    y_bounds = (0.15, 0.2))