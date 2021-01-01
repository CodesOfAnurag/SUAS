import cv2
import numpy as np


 ## Take image in gray scale no matter what.

## If not, Convert it to gray scale
img = cv2.imread('R.PNG',0)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 5)

dilation = cv2.dilate(img,kernel,iterations = 5)

lol= cv2.subtract(dilation,erosion)

lol2 = cv2.subtract(img,lol)

dilation2 = cv2.dilate(lol2,kernel,iterations = 2)


opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
cv2.imshow("original",img)
cv2.imshow("erosion",erosion)
cv2.imshow("dilation",dilation)
cv2.imshow("opening",opening)
cv2.imshow("LOL",lol)
cv2.imshow("lol2",lol2)
cv2.imshow("dilation2",dilation2)

cv2.waitKey(0)
cv2.destroyAllWindows()
