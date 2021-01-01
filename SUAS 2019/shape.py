

# THIS IS NOT THE FINAL CODE, IT WILL BE UPDATED WHENEVER I FIND A BETTER APPROACH FOR THE TASK.

import numpy as np
import cv2
import time

def execute(img):

	blur = cv2.GaussianBlur(img,(5,5),0)
	smooth = cv2.addWeighted(blur,1.5,img,-0.5,0)
	image=smooth

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	ret,thresh = cv2.threshold(gray,20,255,0)

	_,cnts,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#print "contours="+str(len(cnts))

	moments = cv2.moments(cnts[0], True)
	Hu_moments = cv2.HuMoments(moments)
	log_hu= -np.sign(Hu_moments)*np.log10(np.abs(Hu_moments))
	#print log_hu

	area1=cv2.contourArea(cnts[0])
	# min enclosing circle
	(x,y),radius = cv2.minEnclosingCircle(cnts[0])
	center = (int(x),int(y))
	radius = int(radius)
	area2=3.14*radius*radius

	if area2!=0:
		ratio=area1/area2   #comparing contour area and min enclosing circle area
	else:

		ratio=1
		
	#print "ratio="+str(ratio)    

	#function for shape detection 
	def detectShape(cnts):
		shape = 'unknown'
		peri = cv2.arcLength(cnts,True)

		vertices = cv2.approxPolyDP(cnts,0.03*peri,True)
		img = cv2.drawContours(image, vertices, -1, (0,0,255), 3)
		
		#check if circle 
		circles = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
		if circles is not None:
		    shape="circle"
		else:
		     #triangle
		    if len(vertices) == 3:
		        shape = 'triangle'

		     #square/ reactangle/trapezoid?
		    elif len(vertices) == 4:
		        if (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>2.0 and log_hu[1][0] <3.0)  and (log_hu[2][0]>3.0 and log_hu[2][0]<3.6):
		             shape="quater circle"
		        elif (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>1.0 and log_hu[1][0] <2.5)  and (log_hu[2][0]>5.0 and log_hu[2][0]<7.0) and (log_hu[3][0]>6.0 and log_hu[3][0]<8.0):
		            shape = "rectangle"
		        else:
		            x,y,width,height = cv2.boundingRect(vertices)
		            aspectRatio = float(width)/height
		            print "aspect ratio="+str(aspectRatio)
		            if aspectRatio >= 0.4 and aspectRatio <= 0.6:
		                shape="square"
		            else:
		                shape = "trapezoid"


		    elif len(vertices) == 5:
		        if (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>1.0 and log_hu[1][0] <2.5)  and (log_hu[2][0]>5.0 and log_hu[2][0]<7.0) and (log_hu[3][0]>6.0 and log_hu[3][0]<8.0):
		                    shape = "rectangle"
		        elif ratio>0.4 and ratio<0.62:

		            if (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>2.0 and log_hu[1][0] <3.0)  and (log_hu[2][0]>3.0 and log_hu[2][0]<3.6):
		                shape="quater circle"
		            else:
		                shape="semicircle"
		        else:
		            shape="pentagon"
		            

		    elif len(vertices) == 6:
		        if ratio>0.4 and ratio<0.62:
		            if (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>2.0 and log_hu[1][0] <3.0)  and (log_hu[2][0]>3.0 and log_hu[2][0]<3.6):
		                shape="quater circle"
		            else:
		                shape="semicircle"
		        else:
		            shape="hexagon"
		        
		    elif len(vertices) == 7:
		        shape = "heptagon"

		    elif len(vertices) == 8:
		        if ratio>0. and ratio<1.1:
		            shape="circle"
		        else:
		            shape="octagon"
		        
		    
		    elif len(vertices)==13 or (len(vertices) == 12 or  len(vertices)==11):
		        shape = "cross"
		    elif (log_hu[0][0]>0.4 and log_hu[0][0]<1.0) and (log_hu[1][0]>2.0 and log_hu[1][0] <3.0)  and (log_hu[2][0]>3.0 and log_hu[2][0]<3.6):
		        shape="quater circle"
		    elif ratio>0.4 and ratio<0.6 and log_hu[1][0]<2.1:
		        shape = "semicircle"
		    elif ratio>0.9 and ratio<1.1:
		        shape = "circle"

		    else:
		        if (log_hu[0][0]>0.0 and log_hu[0][0]<1.0) and (log_hu[1][0]>4.0 and log_hu[1][0] <5.0)  and (log_hu[2][0]>5.0 and log_hu[2][0]<6.0) and (log_hu[3][0]>6.0 and log_hu[3][0]<7.0):
		            shape = "cross"
		        elif (log_hu[0][0]>0.6 and log_hu[0][0]<1.0) and (log_hu[1][0]>4.2 and log_hu[1][0] <6.0)  and (log_hu[2][0]>5.0 and log_hu[2][0]<6.0) and (log_hu[3][0]>6.0 and log_hu[3][0]<8.0):
		            shape = "star"  
		        else:
		            shape="UNKNOWN"     

		return shape

	# call detectShape 
	final_shape = detectShape(cnts[0])

	return final_shape

