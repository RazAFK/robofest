import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))

def comand(com, *args):
    return str(com)+'#'+'#'.join(list(map(str, args)))

print(comand('abs', 1, 2, 3))