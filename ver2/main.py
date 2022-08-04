import cv2
import serial
from time import sleep
from tool import cam
import numpy as np

COM_PORT = 'COM3'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)

kernel = np.ones((7,7), np.uint8)

cap = cam()
while(1):
    img1, img2 = cap.read2img(ser, delay=0.001)

    img_a = cv2.subtract(img1, img2)
    img_b = cv2.subtract(img2, img1)
    img = cv2.add(img_a, img_b)

    img = cv2.subtract(img, 5)
    img = cv2.multiply(img , 10)

    img = cv2.erode(img, kernel, iterations = 1)
    img = cv2.dilate(img, kernel, iterations = 1)

    cv2.imshow("img", img)
    cv2.imshow("img1", img_a)
    cv2.imshow("img2", img_b)
    cv2.waitKey(30)

# while(1):
#     for s in range(2):
#         if s == 0:
#             ser.write(b'on\n')
#             sleep(0.15)
#             img = cap.read()
#             img = cv2.rotate(img, cv2.ROTATE_180)

#             img = img[:,230:1030,:]

#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             gray = cv2.blur(gray, (10,10))
#             cv2.imshow("img1", gray)
        
#         if s == 1:
#             ser.write(b'off\n')
#             sleep(0.15)
#             img = cap.read()
#             img = cv2.rotate(img, cv2.ROTATE_180)

#             img = img[:,230:1030,:]

#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             gray = cv2.blur(gray, (10,10))
#             cv2.imshow("img2", gray)
#         cv2.waitKey(1)
