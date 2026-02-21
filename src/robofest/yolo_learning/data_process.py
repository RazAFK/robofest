import cv2, threading, os

path = 'C:/Users/admin/Desktop/wroom_wroom/'
form = '.jpg'

cur_dir = os.path.dirname(os.path.abspath(__file__))

ret_dir = os.path.abspath(path)
os.makedirs(ret_dir, exist_ok=True)


# frame = cv2.imread(path+str(i)+form)

running = True

found_classes = {}

# def _update_loop():
#     global rects
#     while running:
#         for rect in rects:
#             cv2.rectangle(frame, rect[0], rect[-1], (0, 255, 0), 2)
#         cv2.imshow('frame', frame)
#         cv2.waitKey(1) & 0xFF
# thread = threading.Thread(target=_update_loop, daemon=True)
# thread.start()

def get_rects():
    global found_classes, path, form, run_thread, i
    frame = cv2.imread(path+str(i)+form)
    cv2.imshow(str(i), frame)
    rects = cv2.selectROIs(str(i), frame, showCrosshair=True, fromCenter=False)
    found_classes[i]=rects
    print(found_classes)
    cv2.destroyWindow(str(i))
    run_thread = False
    i+=1


i = int(input('введите номер с которого начнётся разметка: '))
run_thread = False
while i<5:
    if not run_thread:
        thread = threading.Thread(target=get_rects, daemon=True)
        thread.start()
        run_thread = True

thread_run = True
drowing_rect = ()

def drow_rects(image):
    global thread_run, drowing_rect
    while thread_run:
        if drowing_rect!=():
            cv2.rectangle(image, drowing_rect[0], drowing_rect[-1], (0, 255, 0), 2)
        cv2.imshow('image', image)
        cv2.waitKey(1)

for key, value in zip(found_classes.keys(), found_classes.values()):
    with open(os.path.join(ret_dir, f'{key}.txt'), 'w') as file:
        print(f'сейчас обрабатывается:', key)
        thread = threading.Thread(target=get_rects, daemon=True)
        thread.start()
        image = cv2.imread(path+str(key)+form)

        thread = threading.Thread(target=drow_rects, daemon=True, args=[image])
        thread.start()

        h_img, w_img, _ = image.shape
        for rect in value:
            x, y, w, h = rect

            drowing_rect = ((x, y), (x+w, y+h))

            x_center = (x + w/2) / w_img
            y_center = (y + h/2) / h_img
            norm_w = w / w_img
            norm_h = h / h_img
            print('''Выбери класс(цифру):\n0: склад с кубами(циановый с кубиками или белыми квадратами)\n1: склад для кубов(серый с цифрами)\n2: круговое движение\n3: парковка(зелёная с буквой Р)''')
            cls_name = input()
            while cls_name not in ['1', '2', '3', '0']:
                print('неверный номер, впиши ещё раз')
                cls_name = input()
            print(f'в файл записано: {cls_name} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}')
            file.write(f'{cls_name} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}\n')
        
        thread_run = False
        cv2.destroyWindow('image')
print('молодец, всё готово')
cv2.destroyAllWindows()