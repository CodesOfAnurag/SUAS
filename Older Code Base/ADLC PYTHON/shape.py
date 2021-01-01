import cv2
import numpy as np

source = cv2.imread("/home/manohar/Outputs/Targets/m-0.PNG",1)

graySource = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(graySource,(5,5),0)

ret,thresholdOutput = cv2.threshold(graySource,127,255,cv2.THRESH_BINARY)

im2, contours, hierarchy = cv2.findContours(thresholdOutput,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
contoursize =  len(contours)
print contoursize

contourArea = cv2.contourArea(cnt)
print contourArea

if((contoursize > 0) and (contourArea > 500)):
	cv2.drawContours(source, contours, -1, (0,255,0), 3) #Source to be replaced by drawing2 which is  mat::zeros and get the params right

	circles = cv2.HoughCircles(source,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
#again, set right params and img to drawing2
	circles_size = len(circles)
	
	if(circles_size!=0):
		isCircle = True
	else:
		isCircle = False
		
	
	

cv2.imshow("IMG",thresholdOutput)
cv2.waitKey()
cv2.destroyAllWindows()

