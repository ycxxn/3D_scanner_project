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


def deal_depth2yz(depth):
    yz = []
    y = np.where(depth!=None)[0]
    for yi in y:
        z = depth[yi]
        yz.append([yi, z])
        # print(x,yi)
    # print(xy)
    return np.array(yz)

cap = cam()
while(1):

    depth, mask = cap.read2img_2(ser)

    yz = deal_depth2yz(depth)
    print(yz)

    cv2.imshow("mask", mask)
    cv2.waitKey(1)