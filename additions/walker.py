import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:sys.path.append(project_root)

from connector.arduino_class import Queue, take_arduinos, States

wheels, manipulator = take_arduinos()

wheels_queue = Queue(wheels)
wheels_queue.start_thread()

if wheels is None:
    raise NameError('Гоша, ты чмо, у тебя не подключилась колёсная база')

dict_comand = {
    'mf': wheels.move_forward_time,
    'mb': wheels.move_backward_time,
    'rtr': wheels.roatate_right_time,
    'rtl': wheels.roatate_left_time,
    'st': wheels.move_stop,
    'rt': manipulator.rotateRail,
    'chg': wheels.change_speed
}

comands = []

with open('additions/comands.txt', 'r') as file:
    for line in file:
        com = line.split('#')
        comands.append((dict_comand[com[0]], list(map(int, com[1:]))))
i = 0
moveflag = True
while True:
    data = wheels_queue.get_data_nowait()
    if data and data.check_state(States.moveDone):
        i+=1
        moveflag = True
    if moveflag:
        comands[i][0](*comands[i][-1])
        moveflag = False