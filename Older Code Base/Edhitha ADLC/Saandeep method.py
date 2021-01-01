import cv2
import numpy as np


 ## Take image in gray scale no matter what.

## If not, Convert it to gray scale
img = cv2.imread('I.PNG',0)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 5)

dilation = cv2.dilate(img,kernel,iterations = 5)


ie = cv2.subtract(img,erosion)
idi = cv2.subtract(dilation,img)
cv2.imshow("Erosub",ie)
cv2.imshow("dilsub",idi)
cv2.waitKey(0)
cv2.destroyAllWindows()
