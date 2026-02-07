from robofest.classes.arduino_class import Arm
import time
from robofest.classes.queue_class import Queue

temp_ard = Arm('COM4')
temp_q = Queue(temp_ard)

temp_ard.move_arm(10, 10)
time.sleep(50)