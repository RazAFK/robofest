import cv2

cap = cv2.VideoCapture(0)

def write_file(folder, name):
    for i in range(20):
        ret, frame = cap.read()
    cv2.imwrite(f'additions/photos/{colors[folder]}/{name}.jpg', frame)

colors = {
    'b': 'blue',
    'r': 'red',
    'w': 'white',
    'y': 'yellow',
    'p': 'paper'
}
flag = True
colorsn = {
    'b': 1,
    'r': 1,
    'w': 1,
    'y': 1,
    'p': 1
}
while flag:
    line = input(f'color:\n')
    if line=='stop':
        break
    for i in range(2):
        write_file(line, colorsn[line])
        colorsn[line]+=1