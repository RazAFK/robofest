import cv2

frame = cv2.imread(r'D:\AudioBooks\HarryPotter\Rowling.J._Harry_Potter_i_taynaya_komnata.[torrents.ru]\cover.jpg')

while True:
    cv2.imshow('frame', frame)