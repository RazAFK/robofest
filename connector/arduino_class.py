import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)


import serial, serial.tools.list_ports, time, datetime
from settings.settings import Comands, Plates

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports()]

class Comand:
    def __init__(self, name: Comands, args = []):
        self.name = name
        self.args = list(map(str, args))

    def __str__(self):
        return self.name + '#' + '#'.join(self.args)

class Arduino:
    def __init__(self, port: str, baudrate=9600, timeout=0.1, connection=None, plate = Plates.undefined):
        self.port = port if (os.name!='posix' and connection) else '/dev/'+port
        self.arduino = connection if connection else serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout)
        self.plate = plate
        time.sleep(2)
    
    def write_com(self, comand: Comand):
        bite_comand = f'{comand}\n'.encode()
        self.arduino.write(bite_comand)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8')
        return answer
    
    def define_plate(self):
        self.write_com(Comand(Comands.getPlate))
        answer = self.read_com()

        for plate in Plates:
            if plate in answer:
                self.plate = plate
                return plate
        return Plates.undefined
    
    @classmethod
    def from_existing(cls, old_instance):
        return cls(old_instance.port, connection=old_instance.arduino, plate=old_instance.plate)

    def __str__(self):
        return f'{self.plate} on port {self.port}'

class Wheels(Arduino):
    def move_forward_time(self, milliseconds):
        comand = Comand(Comands.moveForward, [milliseconds])
        self.write_com(comand)

    def move_backward_time(self, milliseconds):
        comand = Comand(Comands.moveBackward, [milliseconds])
        self.write_com(comand)

    
    def move_forward_distance(self, santimetrs):
        pass

    def move_backforward_distance(self, santimetrs):
        pass

class Manipulator(Arduino):
    pass


def take_arduinos():
    ports = get_available_ports()

    arduinos = []

    for port in ports:
        try:
            arduinos.append(Arduino(port))
        except:
            continue
    
    manipulator, wheels = None, None

    for arduino in arduinos:
        if arduino.define_plate()==Plates.manipulator:
            manipulator = Manipulator.from_existing(arduino)
        if arduino.define_plate()==Plates.wheels:
            wheels = Wheels.from_existing(arduino)
    
    return wheels, manipulator
