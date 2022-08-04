import cv2
import numpy as np

cap = cv2.VideoCapture(0)
n = 0
new_img = np.zeros((480,640,3))
while(1):
    ret, img = cap.read()
    print(img.shape)
    new_img[n,:,:] = img[n,:,:]
    img[:n,:,:] = new_img[:n,:,:]
    cv2.line(img, (0, n), (640, n), (0, 0, 255), 5)

    img = cv2.flip(img, 1)
    cv2.imshow("windows", img)
    cv2.waitKey(1)
    n+=1
    if n == 480:
        n = 0