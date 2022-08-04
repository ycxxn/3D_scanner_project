import cv2
from cv2 import Scharr
import numpy as np
import serial
from time import sleep
from tool import cam  

COM_PORT = 'COM5'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)
ser.write(b"off\n")
print("---init----")
sleep(1)
print("Done!")

cap = cam()
delay = 0.15
while(1):
    ser.write(b"move\n")
    sleep(0.5)

    ser.write(b"on\n")
    sleep(delay)
    img_p = cap.read()

    ser.write(b"off\n")
    sleep(delay)
    img_n = cap.read()
    
    img = cv2.subtract(img_p, img_n)
    img = cv2.subtract(img, 30)

    h,w = img.shape[:2]
    x = 300
    img = img[:, x:w-x,:]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.multiply(gray, 5)

    th = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.erode(th, kernel, iterations = 1)
    cv2.imshow("img", img)
    

    l = []
    for n in range(mask.shape[0]):
        c = np.where(mask[n,:]==255)[0]
        if len(c) == 0 or min(c) >= 320:
                l.append(None)
        else:
            length = 68*(320-min(c))/110
            length = round(length, 2)
            l.append(length)
    print(l)
    l = np.array(l)
    print(np.where(l!=None))
    h,w = mask.shape[:2]
    cv2.line(mask, (int(w/2),0), (int(w/2),h), (255), 1)
    # print(min(mask[360,:].index(255)))
    # cv2.imshow("gray", gray)
    cv2.imshow("gray2", gray2)
    cv2.imshow("th", th)
    cv2.imshow("mask", mask)
    cv2.waitKey(1)

    # data = ser.readline()
    # print(data)
    # data = data.decode()
    # while ser.in_waiting:
    #     mcu_feedback = ser.readline().decode()  # 接收回應訊息並解碼
    #     print('控制板回應：', mcu_feedback)
    #     ser.write(b"move\n")

    # print(data) 
    # ser.write(b"move\n")
    # sleep(0.1)
    # print(123)
    # sleep(0.005)

    # ser.write(b"on\n")
    # sleep(delay)
    # img_p = cap.read()
    # img_p = cv2.blur(img_p, (5,5))

    # ser.write(b"off\n")
    # sleep(delay)
    # img_n = cap.read()
    # img_n = cv2.blur(img_n, (5,5))

    # img = cv2.subtract(img_p, img_n)
    # img = cv2.subtract(img, 10)

    # h,w = img.shape[:2]
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.line(img, (int(w/2),0), (int(w/2),h), (0, 255, 0), 1)
    # cv2.line(gray, (int(w/2),0), (int(w/2),h), (255), 1)

    # cv2.imshow("img_p", img_p)
    # cv2.imshow("img_n", img_n)
    # cv2.imshow("img", img)
    # cv2.imshow("gray", gray)

    # ser.write(b"move\n")
    # sleep(0.2)

    # cv2.waitKey(1)