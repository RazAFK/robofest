from __future__ import annotations

import serial, serial.tools.list_ports, queue, threading, datetime, math
import os, time
from enum import StrEnum


from robofest.settings import settings as st

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports() if 'COM' in port.name or 'USB' in port.name]

class Object:
    def __init__(self, time: datetime.datetime, responce: str):
        self.time = time
        self.responce = responce

    def __str__(self):
        return f'{self.time}: {self.responce}'
    
    def check_pref(self, prefix: st.Prefixes):
        return prefix in self.responce

class Arduino:

    def convert_command(self, name, *args):
        return name + st.separator + st.separator.join(list(map(str, args))) + st.separator
    
    def __init__(self, port: str, baudrate=st.arduino_baudrate, timeout=st.arduino_timeout):
        self.port = port
        self.queue = queue.Queue(st.queue_size)
        self.whe = self.Whe(self)
        self.arm = self.Arm(self)

        if os.name=='posix' and ('/dev/' not in port):
            self.port = '/dev/'+port
        self.arduino = serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout)
        time.sleep(st.arduino_init_delay)

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def __str__(self):
        return f'arduino on port: {self.port}'

    def write_com(self, command):
        self.arduino.reset_input_buffer()
        
        bite_command = f'{command}\n'.encode()
        self.arduino.write(bite_command)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8', errors='ignore').strip()
        return answer
    
    def _update_loop(self):
        while self.running:
            data = self.read_com()
            if data:
                if st.Prefixes.data in str(data):
                    data = Object(datetime.datetime.now(), data)
                    self.queue.put(data)
            time.sleep(st.queue_delay)

    def get_data(self) -> Object|None:
        try: return self.queue.get_nowait()
        except queue.Empty: return None

    class Whe:
        class Commands(StrEnum):
            moveForward = 'moveForward'
            moveBackward = 'moveBackward'
            wheelsStop = 'wheelsStop'
            rotateRight = 'rotateRight'
            rotateLeft = 'rotateLeft'
        
        def __init__(self, master: Arduino):
            self.master = master

        def move_stop(self):
            command = self.master.convert_command(self.Commands.wheelsStop)
            self.master.write_com(command)

        def move_forward_distance(self, distance):
            command = self.master.convert_command(self.Commands.moveForward,
                st.velocity_front_right,
                st.velocity_front_left,
                st.velocity_backward_right,
                st.velocity_backward_left,
                distance
                )
            self.master.write_com(command)

        def move_backward_distance(self, distance):
            command = self.master.convert_command(self.Commands.moveBackward,
                st.velocity_front_right,
                st.velocity_front_left,
                st.velocity_backward_right,
                st.velocity_backward_left,
                distance
                )
            self.master.write_com(command)

        def rotate_right(self, distance):
            # distance = degrees*2*st.robot_radius*math.pi/360
            command = self.master.convert_command(self.Commands.rotateRight,
                st.velocity_front_right,
                st.velocity_front_left,
                st.velocity_backward_right,
                st.velocity_backward_left,
                distance,
                )
            self.master.write_com(command)

        def rotate_left(self, distance):
            # distance = degrees*2*st.robot_radius*math.pi/360
            command = self.master.convert_command(self.Commands.rotateLeft,
                st.velocity_front_right,
                st.velocity_front_left,
                st.velocity_backward_right,
                st.velocity_backward_left,
                distance,
                )
            self.master.write_com(command)
        


    class Arm:
        class Commands(StrEnum):
            moveArm = 'moveArm'
        
        def __init__(self, master: Arduino):
            self.master = master

        def move_manipulator(self, x, y):
            command = self.master.convert_command(self.Commands.moveArm, x, y)
            self.master.write_com(command)

