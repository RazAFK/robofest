import serial.tools.list_ports, datetime

from robofest.classes.arduino_class import Arduino, Arm, Wheels, Plates
from robofest.classes.queue_class import Queue

def get_available_ports():
    return [port.name for port in serial.tools.list_ports.comports()]

def init_arduino() -> tuple[Arm, Queue, Wheels, Queue]:
    ports = get_available_ports()
    print(ports)
    found_devices = {}

    for port in ports:
        temp_ard = Arduino(port)
        temp_q = Queue(temp_ard)
        start_time = datetime.datetime.now()
        name = None
        temp_ard.write_com(temp_ard.Comands.getPlate)
        
        while datetime.datetime.now() - start_time <= datetime.timedelta(seconds=2):
            if not temp_q.data_queue.empty():
                name = temp_q.get_data()
                break
        temp_q.running = False
        if name is not None and Plates.manipulator in str(name):
            arm = Arm(port, connection=temp_ard.arduino)
            arm_q = Queue(arm)
            found_devices[Plates.manipulator] = (arm, arm_q)
        elif name is not None and Plates.wheels in str(name):
            wheels = Wheels(port, connection=temp_ard.arduino)
            wheels_q = Queue(wheels)
            found_devices[Plates.wheels] = (wheels, wheels_q)
    
    arm, arm_q = found_devices.get(Plates.manipulator, (None, None))
    wheels, wheels_q = found_devices.get(Plates.wheels, (None, None))

    return arm, arm_q, wheels, wheels_q

