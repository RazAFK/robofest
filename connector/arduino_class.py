import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)


import serial, serial.tools.list_ports, time, datetime
from enum import StrEnum

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports()]


class Plates(StrEnum):
    manipulator = 'manipulator'
    wheels = 'wheels'
    undefined = 'undefined'


class Arduino:

    class Comands(StrEnum):
        getPlate = 'getPlate'

    def convert_comand(self, name: Comands, args=[]):
        return name + '#' + '#'.join(args)

    def __init__(self, port: str, baudrate=9600, timeout=0.1, connection=None, plate = Plates.undefined):
        self.port = port
        if os.name=='posix' and ('/dev/' not in port):
            self.port = '/dev/'+port
        if connection:
            self.arduino = connection
        else:
            self.arduino = serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout)
            time.sleep(1)
        self.plate = plate
    
    def write_com(self, comand):
        bite_comand = f'{comand}\n'.encode()
        self.arduino.write(bite_comand)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8')
        return answer
    
    def define_plate(self):
        comand = self.convert_comand(self.Comands.getPlate)
        self.write_com(comand)
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

    class Comands(StrEnum):
        moveForward = 'moveForward'
        moveBackward = 'moveBackward'
    
    def define_plate(self):
        pass

    def move_forward_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.moveForward, [milliseconds])
        self.write_com(comand)

    def move_backward_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.moveBackward, [milliseconds])
        self.write_com(comand)

    def move_forward_distance(self, santimetrs):
        pass

    def move_backforward_distance(self, santimetrs):
        pass
    
class Manipulator(Arduino):

    class Comands(StrEnum):
        moveVerRail = 'moveVerRail'
        moveHorRail = 'moveHorRail'
        rotateManipulator = 'rotateManipulator'
        grabManipulator = 'grabManipulator'
        rotateRail = 'rotateRail'
        reset = 'reset'

    def define_plate(self):
        pass
    
    def reset(self):
        comand = self.convert_comand(self.Comands.reset, [])
        self.write_com(comand)


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
        if arduino.define_plate()==Plates.wheels:
            wheels = Wheels.from_existing(arduino)
        if arduino.define_plate()==Plates.manipulator:
            manipulator = Manipulator.from_existing(arduino)
    if wheels==None or manipulator==None:
        for arduino in arduinos:
            if arduino.define_plate()==Plates.manipulator:
                manipulator = Manipulator.from_existing(arduino)
            if arduino.define_plate()==Plates.wheels:
                wheels = Wheels.from_existing(arduino)
    
    return wheels, manipulator
