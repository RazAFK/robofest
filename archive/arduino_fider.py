import os, serial, serial.tools.list_ports, time, datetime

system = ''
if os.name=='posix':
    system = '/dev/'

plates = ['manipulator', 'wheels']

def write_com(arduino):
    arduino.write(b'getPlate\n')

def read_com(arduino):
    data = arduino.readline().decode('utf-8')
    return data

ports = [system+port.name for port in serial.tools.list_ports.comports()]


arduino = serial.Serial(port=ports[0], baudrate=9600, timeout=0)
time.sleep(1)
start = datetime.datetime.now()
# ret = read_com(arduino)
# while plates[-1] not in ret:
write_com(arduino)
ret = read_com(arduino)
end = datetime.datetime.now()
print(ret, end-start)

start = datetime.datetime.now()
write_com(arduino)
ret = read_com(arduino)
end = datetime.datetime.now()
print(ret, end-start)