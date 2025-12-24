import os, serial, serial.tools.list_ports, time, datetime

plates = ['main', 'wheels']

def write_com(arduino):
    arduino.write(b'getPlate#0\n')

def read_com(arduino):
    data = arduino.readline().decode('utf-8')
    return data

ports = [(port.description, f"{port.vid:04X}" if port.vid else "", f"{port.pid:04X}" if port.pid else "") for port in serial.tools.list_ports.comports()]

print(*ports, sep='\n')
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

