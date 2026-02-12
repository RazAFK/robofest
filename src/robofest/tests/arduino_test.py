import datetime

from robofest.classes.arduino_class import Arduino, get_available_ports 


ports = get_available_ports()
print('ports:', ports)
start = datetime.datetime.now()
ard = Arduino(ports[0])
print('arduino init:', datetime.datetime.now()-start)

start = datetime.datetime.now()
ard.whe.move_forward_time(1000)
print('command send:', datetime.datetime.now()-start)

start = datetime.datetime.now()
data = ard.get_data()
while data is None:
    data = ard.get_data()
print('data got:', data.responce)
print('data got:', datetime.datetime.now()-start)