import cv2
import numpy as np
from tool import cam

cap = cam()

n = 1
while(1):
    img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)
    img = img[:,230:1030,:]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (10,10))

    if n%2 == 0:
        img1 = np.copy(gray)
    if n%2 == 1:
        img2 = np.copy(gray)

    if n > 2:
        res1 = cv2.subtract(img1, img2)
        res2 = cv2.subtract(img2, img1)

        res = cv2.add(res1, res2)


        cv2.imshow("res", res)
        cv2.imshow("123", img)
        cv2.waitKey(30)

    n+=1