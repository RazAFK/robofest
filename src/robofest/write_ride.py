from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.arduino_class import Arduino, get_available_ports

from robofest.functions.center_handler import get_center_contour, get_storage_centers
from robofest.functions.lines_handler import handl_lines
from robofest.functions.num_handler import handl_num
from robofest.functions.math_funcs import get_step_angle, get_coords

avaliable_ports = get_available_ports()
arduino = Arduino(avaliable_ports)

def execute_command(executor, command, *args):
    try:
        getattr(executor, command)(*args)
        return f'[DOING] {command} with args {args}'
    except:
        return f'[ERROR] {command} with args {args}'

def check_command(command):
    try:
        func, executor = getattr(arduino.whe, command), arduino.whe
    except:
        try:
            func, executor = getattr(arduino.arm, command), arduino.arm
        except:
            return False
    return callable(func), executor


while True:
    com = input()
    if com=='exit':
        break
    if com=='load':
        print('[INFO] start loaded program')
        print('[INFO] loading script')
        with open('ride.txt') as file:
            commands = []
            for line in file:
                command, *args = com.split('#')
                ret, exc = check_command(command)
                if ret:
                    commands.append((exc, command, args))
                else:
                    print(f'[WARN] failed to load {command} with args {args}')
        print('[INFO] load end')
        if len(commands)==0:
            print('[INFO] no commands to execute')
        else:
            print('[INFO] executing started')
            it = iter(commands)
            working_flag = False
            worker = next(it)
            while True:
                if working_flag:
                    data = arduino.get_data()
                    if st.Prefixes.move_done in data:
                        working_flag = False
                    try:
                        worker = next(it)
                    except:
                        break
                if not working_flag:
                    execute_command(worker[0], worker[1], worker[-1])
                    working_flag = True
            print('[INFO] executing ended')
        print('[INFO] end loaded program')
    command, *args = com.split('#')
    ret, exc = check_command(command)
    if ret:
        execute_command(exc, command, args)