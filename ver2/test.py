import cv2
from tool import cam

cap = cam()

n = 1
while(1):
    img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)

    img = img[:,230:1030,:]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (10,10))

    # cv2.line(gray,(0,360),(1280,360),(0,255,0),1)#绿色，3个像素宽度
    cv2.imshow("img", gray)

    key = cv2.waitKey(1)

    if key ==ord("s"):
        cv2.imwrite(str(n)+"_1.jpg", gray)
        n+=1