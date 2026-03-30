from robofest.scenes.alignment import levelout_angle
from robofest.classes.camera_class import Camera
from robofest.classes.limit_class import Limits

levelout_angle(Camera(0), 123, 123, Limits(sizes=(640, 480), length=(150, 1000), angle=(0, 90)), 123)