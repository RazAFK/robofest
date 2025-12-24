import cv2

cap = cv2.VideoCapture(1)

def write_file(folder, name):
    for i in range(10):
        ret, frame = cap.read()
    cv2.imwrite(f'photos/{colors[folder]}/{name}.jpg', frame)

colors = {
    'b': 'blue',
    'r': 'red',
    'w': 'white',
    'y': 'yellow'
}
flag = True
colorsn = {
    'b': 1,
    'r': 1,
    'w': 1,
    'y': 1
}
while flag:
    line = input(f'color:\n')
    if line=='stop':
        break
    write_file(line, colorsn[line])
    colorsn[line]+=1