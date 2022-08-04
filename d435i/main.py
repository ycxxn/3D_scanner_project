import cv2
from cv2 import Scharr
import serial
from time import sleep
from tool import cam  

COM_PORT = 'COM5'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)
ser.write(b"off\n")
print("---init----")
# sleep(1)

cap = cam()
while(1):
    # img1, img2 = cap.read2img(ser, delay=0.15)

    # img = cv2.subtract(img2, img1)
    
    # h, w = img.shape[:2]

    # ret, th = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    # scharrx = cv2.Scharr(th, cv2.CV_32F, 1,0)
    # scharrx = cv2.convertScaleAbs(scharrx)
    # # img = cv2.line(img, (int(w/2), 0), (int(w/2), h), (255), 1)

    # cv2.imshow("img1", img1)
    # cv2.imshow("img2", img2)
    # cv2.imshow("img", img)
    # cv2.imshow("th", th)
    # # cv2.imshow("scharrx",  scharrx)
    # cv2.waitKey(1)
    ser.write(b"on\n")
    sleep(0.5)
    img1 = cap.read()

    ser.write(b"off\n")
    sleep(0.5)
    img2 = cap.read()

    img = cv2.subtract(img1, img2)
    cv2.imshow("img", img)
    cv2.waitKey(1)