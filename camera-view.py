import cv2
from datetime import date, datetime
import time


cv2.namedWindow("preview")

vc = cv2.VideoCapture(1, cv2.CAP_DSHOW) #, cv2.CAP_DSHOW cv2.CAP_V4L2 cv2.CAP_FFMPEG

vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640); #1280 1600
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480); #720 1200

while True:         
    rval, frame = vc.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray,(5,5),0) 
    #ret, thresh = cv2.threshold(blur,20,180,cv2.THRESH_BINARY_INV)
    #sobelxy = cv2.Sobel(src=blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
    edge = cv2.Canny(frame, 50, 150)
    cv2.imshow("preview", edge)
    key = cv2.waitKey(1)
    if key == 115:
        fileName=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg"
        cv2.imwrite(fileName, frame)
        
    if key == 27: # exit on ESC
        break
       
    
cv2.destroyWindow("preview")
vc.release()
