import serial
import os, time
from enum import StrEnum

from robofest.settings import settings as st

class Plates(StrEnum):
    manipulator = 'manipulator'
    wheels = 'wheels'

class Arduino:

    class Comands(StrEnum):
        getPlate = 'getPlate'

    def convert_comand(self, name: Comands, *args):
        return name + '#' + '#'.join(list(map(str, args)))

    def __init__(self, port: str, baudrate=st.arduino_baudrate, timeout=st.arduino_timeout, connection=None):
        self.port = port
        if os.name=='posix' and ('/dev/' not in port):
            self.port = '/dev/'+port
        if connection:
            self.arduino = connection
        else:
            self.arduino = serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout)
            time.sleep(2)

    def write_com(self, comand):
        self.arduino.reset_input_buffer()
        
        bite_comand = f'{comand}\n'.encode()
        self.arduino.write(bite_comand)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8', errors='ignore').strip()
        return answer
    
    def __str__(self):
        return f'arduino on port {self.port}'
    
class Wheels(Arduino):

    class Comands(StrEnum):
        moveForward = 'moveForward'
        moveBackward = 'moveBackward'
        moveStop = 'moveStop'
        changeSpeed = 'changeSpeed'
        rotateRight = 'rotateRight'
        rotateLeft = 'rotateLeft'

    def move_stop(self):
        comand = self.convert_comand(self.Comands.moveStop)
        self.write_com(comand)

    def change_speed(self, s1, s2, s3, s4):
        comand = self.convert_comand(self.Comands.changeSpeed, s1, s2, s3, s4)
        self.write_com(comand)

    def move_forward_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.moveForward, milliseconds)
        self.write_com(comand)

    def move_backward_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.moveBackward, milliseconds)
        self.write_com(comand)

    def move_forward_distance(self, santimetrs):
        pass

    def move_backforward_distance(self, santimetrs):
        pass
    
    def roatate_right_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.rotateRight, milliseconds)
        self.write_com(comand)

    def roatate_left_time(self, milliseconds):
        comand = self.convert_comand(self.Comands.rotateLeft, milliseconds)
        self.write_com(comand)

    def roatate_right_degrees(self, degrees):
        pass

    def roatate_left_degrees(self, degrees):
        pass

class Arm(Arduino):
    
    class Params:
        grab = {True: st.limit_manipulator_open, False: st.limit_manipulator_close}

    class Comands(StrEnum):
        moveVerRail = 'moveVerRail'
        moveHorRail = 'moveHorRail'
        rotateManipulator = 'rotateManipulator'
        grabManipulator = 'grabManipulator'
        rotateRail = 'rotateRail'
        moveManipulator = 'moveManipulator'
        getCoordinates = 'getCoordinates'
    
    def get_coordinates(self):
        comand = self.convert_comand(self.Comands.getCoordinates)
        self.write_com(comand)
    
    def move_arm(self, x, y):
        comand = self.convert_comand(self.Comands.moveManipulator, x, y)
        self.write_com(comand)


    def move_vertical_rail(self, position: int):
        f'''
        ^
        v
        moving

        :param position: [{st.limit_vertical_step[0]}; {st.limit_vertical_step[-1]}]
        '''
        comand = self.convert_comand(self.Comands.moveVerRail, position)
        self.write_com(comand)

    def move_horizontal_rail(self, position: int):
        f'''
        < >
        moving
        
        :param position: [{st.limit_horizontal_step[0]}; {st.limit_horizontal_step[-1]}]
        '''
        comand = self.convert_comand(self.Comands.moveHorRail, position)
        self.write_com(comand)

    def rotate_manipulator(self, degrees: int):
        '''
        rotating manipulator
        
        :param degrees: [0; 180]
        '''
        comand = self.convert_comand(self.Comands.rotateManipulator, degrees)
        self.write_com(comand)

    def grab_manipulator(self, pull: bool):
        '''
        True - manipulator pulls hands
        
        False - manipulator unpulls hands

        :param degrees: True || False
        '''
        comand = self.convert_comand(self.Comands.grabManipulator, self.Params.grab[pull], 0)
        self.write_com(comand)
    
    def grab_close(self):
        self.grab_manipulator(True)

    def grab_open(self):
        self.grab_manipulator(False)

    def rotate_rail(self, degrees: int):
        '''
        rotating rail

        :param degrees: [0; 180]
        '''
        comand = self.convert_comand(self.Comands.rotateRail, degrees)
        self.write_com(comand)