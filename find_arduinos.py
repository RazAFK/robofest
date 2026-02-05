from connector.arduino_class import take_arduinos, Plates, Arduino
from datetime import datetime
from time import sleep

start = datetime.now()

wheels, manipulator = take_arduinos()

print(wheels)
print(manipulator)

end = datetime.now()

print('total time:', end-start)

# arduino = Arduino('COM5')
# sleep(2)
# arduino.start_thread()

# arduino.write_com(arduino.convert_comand(arduino.Comands.getPlate))

# start = datetime.now()
# print(arduino.define_plate())
# end = datetime.now()
# print(end-start)