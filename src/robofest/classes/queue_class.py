import queue, threading, datetime, time

from robofest.settings import settings as st
from robofest.classes.arduino_class import Arduino, Arm, Wheels

class Object:
    def __init__(self, time: datetime.datetime, responce: str):
        self.time = time
        self.responce = responce
        self.type = responce.split(st.separator)[1]
        self.args = list(responce.split(st.separator)[2:])

    def __str__(self):
        return f'{self.time}: {self.responce}'
    
    def check_state(self, prefix: st.Prefixes):
        return prefix in self.responce

class Queue:
    def __init__(self, arduino: Arduino|Arm|Wheels, size=st.queue_size):
        self.arduino = arduino
        self.data_queue = queue.Queue(maxsize=size)

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
    
    def _update_loop(self):
        while True:
            data = self.arduino.read_com()
            if data:
                if st.Prefixes.data in data:
                    data = Object(datetime.datetime.now(), data)
                    self.data_queue.put(data)
            time.sleep(0.01)
    
    def get_data(self) -> Object|None:
        try: return self.data_queue.get_nowait()
        except queue.Empty: return None
