from __future__ import annotations

import serial, serial.tools.list_ports, queue, threading, datetime
import os, time
from enum import StrEnum


from robofest.settings import settings as st

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports()]

class Object:
    def __init__(self, time: datetime.datetime, responce: str):
        self.time = time
        self.responce = responce
        self.type = responce.split(st.separator)[1]
        self.args = list(responce.split(st.separator)[2:])

    def __str__(self):
        return f'{self.time}: {self.responce}'
    
    def check_pref(self, prefix: st.Prefixes):
        return prefix in self.responce

class Arduino:

    class Comands(StrEnum):
        stop = 'Stop'

    def convert_comand(self, name, *args):
        return name + '#' + '#'.join(list(map(str, args)))
    
    def __init__(self, port: str, baudrate=st.arduino_baudrate, timeout=st.arduino_timeout):
        self.port = port
        self.queue = queue.Queue(st.queue_size)
        self.whe = self.Whe(self)
        self.arm = self.Arm(self)

        if os.name=='posix' and ('/dev/' not in port):
            self.port = '/dev/'+port
        self.arduino = serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def write_com(self, comand):
        self.arduino.reset_input_buffer()
        
        bite_comand = f'{comand}\n'.encode()
        self.arduino.write(bite_comand)

    def read_com(self):
        answer = self.arduino.readline().decode('utf-8', errors='ignore').strip()
        return answer
    
    def _update_loop(self):
        while True:
            data = self.read_com()
            if data:
                if st.Prefixes.data in str(data):
                    data = Object(datetime.datetime.now(), data)
                    self.queue.put(data)
            # time.sleep(0.01)

    def get_data(self) -> Object|None:
        try: return self.queue.get_nowait()
        except queue.Empty: return None

    def stop(self):
        comand = self.convert_comand(self.Comands.stop)
        self.write_com(comand)

    class Whe:
        class Comands(StrEnum):
            moveForward = 'moveForward'
            moveBackward = 'moveBackward'
            moveStop = 'moveStop'
        
        def __init__(self, master: Arduino):
            self.master = master

        def move_stop(self):
            comand = self.master.convert_comand(self.Comands.moveStop)
            self.master.write_com(comand)

        def move_forward_time(self, milliseconds):
            comand = self.master.convert_comand(self.Comands.moveForward, milliseconds)
            self.master.write_com(comand)

        def move_backward_time(self, milliseconds):
            comand = self.master.convert_comand(self.Comands.moveBackward, milliseconds)
            self.master.write_com(comand)

    class Arm:
        class Comands(StrEnum):
            moveArm = 'moveArm'
        
        def __init__(self, master: Arduino):
            self.master = master

        def move_manipulator(self, x, y):
            comand = self.master.convert_comand(self.Comands.moveArm, x, y)
            self.master.write_com(comand)

