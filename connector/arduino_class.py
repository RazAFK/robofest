import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

from settings import settings as st

import serial, serial.tools.list_ports, time, datetime, queue, threading
from enum import StrEnum

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports()]

def constrain(x, start, end):
    return x if start<=x<=end else start if x<start else end


class Plates(StrEnum):
    manipulator = 'manipulator'
    wheels = 'wheels'
    undefined = 'undefined'

class Q_obj:
    def __init__(self, time: datetime.datetime, responce):
        self.time = time
        self.responce = responce
    
    def __str__(self):
        return f'{self.time}: {self.responce}'
    

class Arduino:

    class Comands(StrEnum):
        getPlate = 'getPlate'

    def convert_comand(self, name: Comands, *args):
        return name + '#' + '#'.join(list(map(str, args)))

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

        self.data_queue = queue.Queue(maxsize=1)

    def start_thread(self):
        thread = threading.Thread(target=self._update_loop, daemon=True)
        thread.start()
    
    def _update_loop(self):
        while True:
            data = self.read_com()
            if data:
                if self.data_queue.full():
                    try: self.data_queue.get_nowait()
                    except queue.Empty: pass
                data = Q_obj(datetime.datetime.now(), data)
                self.data_queue.put(data)
    
    def get_data_nowait(self):
        try: return self.data_queue.get_nowait()
        except queue.Empty: return None

    def get_data(self, timeout=0.3):
        try: return self.data_queue.get(timeout=timeout)
        except queue.Empty: return None

    def write_com(self, comand):
        bite_comand = f'{comand}\n'.encode()
        self.arduino.write(bite_comand)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8', errors='ignore')
        return answer
    
    def define_plate(self):
        self.arduino.reset_input_buffer()

        comand = self.convert_comand(self.Comands.getPlate)
        self.write_com(comand)
        answer = str(self.get_data())
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
        moveStop = 'moveStop'
        changeSpeed = 'changeSpeed'
        rotateRight = 'rotateRight'
        rotateLeft = 'rotateLeft'
    
    def define_plate(self):
        pass
    
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

class Manipulator(Arduino):
    
    class Params:
        grab = {True: 120, False: 0}

    class Comands(StrEnum):
        moveVerRail = 'moveVerRail'
        moveHorRail = 'moveHorRail'
        rotateManipulator = 'rotateManipulator'
        grabManipulator = 'grabManipulator'
        rotateRail = 'rotateRail'
        reset = 'reset'
        moveManipulator = 'moveManipulator'
        getCoordinates = 'getCoordinates'

    def define_plate(self):
        pass
    
    def reset(self):
        comand = self.convert_comand(self.Comands.reset)
        self.write_com(comand)
    
    def getCoordinates(self):
        return self.get_data()
    
    def moveManipulator(self, x, y):
        comand = self.convert_comand(self.Comands.moveManipulator, x, y)
        self.write_com(comand)


    def moveVerRail(self, position: int):
        f'''
        ^
        v
        moving

        :param position: [{st.arduino_ver_step_limit[0]}; {st.arduino_ver_step_limit[-1]}]
        '''
        comand = self.convert_comand(self.Comands.moveVerRail, constrain(position, st.arduino_ver_step_limit[0], st.arduino_ver_step_limit[-1]), 0)
        self.write_com(comand)
    
    def moveHorRail(self, position: int):
        f'''
        < >
        moving
        
        :param position: [{st.arduino_hor_step_limit[0]}; {st.arduino_hor_step_limit[-1]}]
        '''
        comand = self.convert_comand(self.Comands.moveHorRail, constrain(position, st.arduino_hor_step_limit[0], st.arduino_hor_step_limit[-1]), 0)
        self.write_com(comand)

    def rotateManipulator(self, degrees: int):
        '''
        rotating manipulator
        
        :param degrees: [0; 180]
        '''
        comand = self.convert_comand(self.Comands.rotateManipulator, constrain(degrees, 0, 180), 0)
        self.write_com(comand)

    def grabManipulator(self, pull: bool):
        '''
        True - manipulator pulls hands
        
        False - manipulator unpulls hands

        :param degrees: True || False
        '''
        comand = self.convert_comand(self.Comands.grabManipulator, self.Params.grab[pull], 0)
        self.write_com(comand)

    def rotateRail(self, degrees: int):
        '''
        rotating rail

        :param degrees: [0; 180]
        '''
        comand = self.convert_comand(self.Comands.rotateRail, constrain(degrees, 0, 180), 0)
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
        arduino.start_thread()
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

