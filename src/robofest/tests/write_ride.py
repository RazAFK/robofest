from robofest.settings import settings as st
from robofest.settings import limits_settings as lst

from robofest.classes.arduino_class import Arduino, get_available_ports

import time

avaliable_ports = get_available_ports()
print('[INFO] avaliable_ports', avaliable_ports)
# arduino = Arduino(avaliable_ports[0])
arduino = Arduino('COM4')
print('[INFO] ', arduino)

def execute_command(executor, command, args):
    if executor=='code':
        if command=='delay':
            time.sleep(float(args[0]))
            return f'[DONE] {command} with args {args}'

    try:
        getattr(executor, command)(*args)
        return f'[DOING] {command} with args {args}'
    except Exception as e:
        return f'[ERROR] {command} with args {args}\n[ERROR] {e}'

def check_command(command):
    if command=='delay':
        return True, 'code'
    try:
        func, executor = getattr(arduino.whe, command), arduino.whe
    except:
        try:
            func, executor = getattr(arduino.arm, command), arduino.arm
        except:
            return False, None
    return callable(func), executor

while True:
    com = input('[INPUT] ')
    if com=='exit':
        break
    if com=='com':
        for exc in (arduino.arm, arduino.whe):
            for item in [ x for x in dir(exc) if '__' not in x and callable(getattr(exc, x))]:
                print(f'[INFO] {exc} has attr {item}')
    if com=='load':
        print(f'[INFO] start loaded program')
        print('[INFO] loading script')
        with open('src/robofest/tests/ride.txt') as file:
            commands = []
            for line in file:
                command, *args = line.strip().split('#')
                ret, exc = check_command(command)
                if ret:
                    commands.append((exc, command, args))
                    print(f'[INFO] loaded {command} with args {args} from executor {exc}')
                else:
                    print(f'[WARN] failed to load {command} with args {args}')
        print('[INFO] load end')
        if len(commands)==0:
            print('[INFO] no commands to execute')
        else:
            print('[INFO] executing started')
            for worker in commands:
                print(execute_command(worker[0], worker[1], worker[-1]))

            # it = iter(commands)
            # working_flag = False
            # worker = next(it)
            # while True:
            #     if working_flag:
            #         data = arduino.get_data()
            #         if st.Prefixes.move_done in data:
            #             working_flag = False
            #         try:
            #             worker = next(it)
            #         except:
            #             break
            #     if not working_flag:
            #         execute_command(worker[0], worker[1], worker[-1])
            #         working_flag = True
            print('[INFO] executing ended')
        print('[INFO] end loaded program')
    command, *args = com.split('#')
    ret, exc = check_command(command)
    if ret:
        print(execute_command(exc, command, args))
    else:
        print('[WARN] wrong command')