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

for port in ports:
    arduino = serial.Serial(port=port, baudrate=9600, timeout=0.1)
    time.sleep(2)
    write_com(arduino)
    ret = read_com(arduino)
    while ret!='':
        if plates[0] in ret:
            print(f'{plates[0]} {port}')
            break
        if plates[1] in ret:
            print(f'{plates[1]} {port}')
            break

#print(*ports, sep='\n')
# with open('arduino_ports.txt', 'w') as file:
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         try:
#             arduino = serial.Serial(port=port.device, baudrate=9600, timeout=0.1)
#             time.sleep(2)
#         except:
#             continue
#         print(port.device)
#         write_com(arduino)
#         ret = read_com(arduino)
#         start_time = datetime.datetime.now()
#         now_time = datetime.datetime.now()
#         while ret is None and start_time-now_time<=2:
#             now_time = datetime.datetime.now()
#             ret = read_com(arduino)
#         print(ret, port.device)
#         if plates[0] in ret:
#             file.writelines(f'{plates[0]} {port.device}')
#         else:
#             file.writelines(f'{plates[1]} {port.device}')

