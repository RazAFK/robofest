from robofest.classes.arduino_class import Arm, Arduino
import time
from robofest.classes.queue_class import Queue

temp_ard = Arm('COM3')

temp_ard.write_com(temp_ard.convert_comand(Arduino.Comands.getPlate, 0))
data = temp_ard.read_com()
print(data)
data = temp_ard.read_com()
print(data)

temp_ard.move_arm(10, 10)

data = temp_ard.read_com()
print(data)
data = temp_ard.read_com()
print(data)
data = temp_ard.read_com()
print(data)
# temp_q = Queue(temp_ard)

# time.sleep(50)