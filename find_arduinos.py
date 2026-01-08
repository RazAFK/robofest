from connector.arduino_class import take_arduinos
from datetime import datetime

start = datetime.now()

wheels, manipulator = take_arduinos()

print(wheels)
print(manipulator)

end = datetime.now()

print('total time:', end-start)


