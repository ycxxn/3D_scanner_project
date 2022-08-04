import cv2
import numpy as np
from tool import cam
import time
import matplotlib.pyplot as plt

x1 = np.linspace(0, 1280, 1280)
y1 = np.linspace(0, 10, 1280)
# plt.ion()
# figure, ax = plt.subplots(figsize=(8,6))
# line1, = ax.plot(x1, y1)
fig = plt.figure()


cap = cam()

while(1):
    img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.medianBlur(thresh,11)
    l = []
    for n in range(thresh.shape[1]):
        c = np.where(thresh[:,n]==255)[0]
        if len(c) == 0:
            l.append(-1)
        else:
            # print(n, max(c))
            # l.append(max(c))
            # 42 pixel = 40 mm
            length = 4.0*(max(c)-458)/40
            length = round(length, 2)
            l.append(length)
    
    print(l)
    # line1.set_xdata(x)
    # line1.set_ydata(l)
    # figure.canvas.draw()
    # figure.canvas.flush_events()
    # time.sleep(0.01)

    plt.ylim(-2,10)
    plt.plot(x1,l)
    plt.draw()  
    plt.pause(0.01)
    fig.clear()


    res = cv2.hconcat([cv2.resize(gray, (320,240)),cv2.resize(thresh, (320,240))])
    # cv2.imshow("img", cv2.resize(gray, (320,240)))
    # cv2.imshow("th", cv2.resize(thresh, (320,240)))
    cv2.imshow("res", res)
    cv2.waitKey(1)
