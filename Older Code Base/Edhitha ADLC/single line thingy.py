import cv2
import numpy as np


 ## Take image in gray scale no matter what.

## If not, Convert it to gray scale
img = cv2.imread('S.PNG',0)
size = np.size(img)
Single_Line = np.zeros(img.shape,np.uint8)
 
ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(7,7))
Done_Flag=0

kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 4)

dilation = cv2.dilate(img,kernel,iterations = 4)

lol= cv2.subtract(dilation,erosion)

 ## Use a for loop for less iterations. It gives decent results too

## Try putting the flag for 10 iterations only. You get a weird outline for I
while( Done_Flag == 0):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    Single_Line = cv2.bitwise_or(Single_Line,temp)
    img = eroded.copy()
 
    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        Done_Flag = 1

#kernel = np.ones((5,5),np.uint8)
#Single_Line = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
Single_Line=cv2.subtract(Single_Line,lol)
cv2.imshow("skeleton!!",Single_Line)
#cv2.imshow("opening",opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
