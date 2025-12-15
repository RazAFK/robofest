import serial 
import time 
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)
def write_read(x): 
    arduino.write(bytes(x, 'utf-8'))
    #arduino.write(b'Hello, Arduino!')
    time.sleep(0.9)
    data = arduino.readline().decode('utf-8')
    return data

while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value)