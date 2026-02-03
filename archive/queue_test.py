from connector.arduino_class import *
from datetime import datetime as timer
import cv2

wheels, manipulator = take_arduinos()
print(wheels, manipulator)

wheels_queue = Queue(wheels)
wheels_queue.start_thread()

def nothing(x):
    pass

cv2.namedWindow('Settings')

while True:
    start = timer.now()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('f'):
        wheels.move_stop()
    elif key == ord('e'):
        arduino_sent = timer.now()
        wheels.move_forward_time(5000)
    data = wheels_queue.get_data_nowait()
    if data:
        now = timer.now()
        print(now-start, now-arduino_sent, start-arduino_sent, data)
print(wheels_queue.data_queue.queue)