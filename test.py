import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))

arr = [[0, 1], [1, 10], [-10, 11]]
print(max(arr, key=lambda x: x[0]))