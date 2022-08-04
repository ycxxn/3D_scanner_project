import cv2

# img1 = cv2.imread("1.jpg",0)
# img2 = cv2.imread("2.jpg",0)

img1 = cv2.imread("1_1.jpg",0)
img2 = cv2.imread("2_1.jpg",0)


# img = img1-img
img = cv2.subtract(img2, img1)
img = cv2.subtract(img, 5)
# img = img * 10
img = cv2.multiply(img , 50)
thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]


cv2.imshow("11", img)
cv2.imshow("12", thresh)
cv2.waitKey(0)