import serial, time, threading
from datetime import datetime, timedelta

arduino = serial.Serial('COM4', 9600, timeout=0.1)

time.sleep(2)

bite_command = f'moveForward#1#1#1#1#1#\n'.encode()
arduino.write(bite_command)

def _update_loop():
    start = datetime.now()
    while datetime.now()-start<timedelta(seconds=5):
        data = arduino.readline().decode('utf-8', errors='ignore').strip()
        if data!='':
            print(data)


thread = threading.Thread(target=_update_loop, daemon=True)
thread.start()

start = datetime.now()
while datetime.now()-start<timedelta(seconds=7):
    pass
print('end')