import os
import serial.tools.list_ports


def is_linux():
    system = os.name
    if system=='nt':
        return False
    return True


# if is_linux():
#     ports = None
# else:
#     ports = #sorted([port.device for port in serial.tools.list_ports.comports()])

ports = serial.tools.list_ports.comports()
for port in ports:
    arduino = serial.Serial(port='COM9', baudrate=9600, timeout=0.1)
print(ports)

#arduino = serial.Serial(port='COM9', baudrate=9600, timeout=0.1)


# import serial
# import time

# comands = '''
# getPlate#0\n
# moveForward#MS\n
# moveBackward#MS\n
# '''

# arduino = serial.Serial(port='COM9', baudrate=9600, timeout=0.1)
# time.sleep(2)
# def write_read(x): 
#     #arduino.write(bytes(x, 'utf-8'))
#     arduino.write(b'moveForward#1000\n')
#     time.sleep(0.9)
#     data = arduino.readline().decode('utf-8')
#     return data

# def write_com(com):
#     arduino.write(b'getPlate#0\n')

# def read_com():
#     data = arduino.readline().decode('utf-8')
#     return data

# write_com('s')
# value = read_com()
# while value is None:
#     value = read_com()
# print('wheels' in value)

#print(available_ports)
