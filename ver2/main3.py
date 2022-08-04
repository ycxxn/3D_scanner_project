import cv2
import serial
from time import sleep
from tool import cam
import numpy as np

COM_PORT = 'COM3'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)

cap = cam()

def processing(img1, img2):

    kernel = np.ones((5,5), np.uint8)
    res = cv2.subtract(img2, img1)

    cv2.imshow("1", res)
    res = cv2.subtract(res, 15)
    # res = cv2.add(res, 100)
    res = cv2.multiply(res , 20)
    res = cv2.threshold(res, 70, 255, cv2.THRESH_BINARY)[1]
    res = cv2.erode(res, kernel, iterations = 1)
    # res = cv2.dilate(res, kernel, iterations = 1)

    return res

while(1):
    img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)     
    img = img[:,230:1030,:]

    cv2.imshow("img", img)
    key = cv2.waitKey(1)

    if key == ord("s"):
        img1, img2 = cap.read2img(ser, delay=0.1)

        res = processing(img1, img2)

        img = cv2.hconcat([img1, img2])
        img = cv2.resize(img, (800,360))
        cv2.imshow("img_", img)
        cv2.imshow("res", res)