import cv2
import numpy as np
import cv2.cv as cv

def zeros(image,height,width):
    drawing = np.zeros([height,width],dtype=np.uint8)
    return drawing



image=cv2.imread("Semicircle.PNG",1)
height = np.size(image, 0)
width = np.size(image, 1)


drawing = zeros(image,height,width)
drawing2 = zeros(image,height,width)

#Changing image to grayScale
graySource = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Blurring using Gaussian blur to improve accuracy of finding contours
blurred = cv2.GaussianBlur(graySource,(5,5),0)

#Thresholding the bit values
ret,thresholdOutput = cv2.threshold(graySource,60,255,cv2.THRESH_BINARY)
#Finding external contour from the image
contours, hierarchy = cv2.findContours(thresholdOutput,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#finding contour size
contours_size = len(contours)
print contours_size
#finding contour area
cnt = contours[0]
contours_area = cv2.contourArea(cnt)
print contours_area

if( (contours_size>0) and (contours_area>500) ):
    print "entered loop"
    cv2.drawContours(drawing2,contours,-1,(0,255,0),3)
    #cv2.imshow("drawing2",drawing2)
    circles = cv2.HoughCircles(drawing2,cv.CV_HOUGH_GRADIENT,1,60,param1=200,param2=20,minRadius=15,maxRadius=0)
    if circles is not None:
        isCircle = True
        #need to draw it
        for i in circles[0,:]:
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    else:
        isCircle = False

print isCircle


perimeter = cv2.arcLength(cnt,True)

print ("Perimeter:",perimeter)


contours_poly = cv2.approxPolyDP(cnt, perimeter * 0.04 , True )
print len(contours_poly)

isConvex = cv2.isContourConvex(contours_poly)

print ("isConvex",isConvex)
#Drawing the lines of the approximated contour using 'line' function on drawing matrix

# Drawing yet to be done
m = cv2.moments(cnt,True);
m2 = cv2.moments(drawing,True);


ans = cv2.HuMoments(m)
ans2 = cv2.HuMoments(m2)

mValu = ans[0]
mValue2 = ans[1]
mValue3 = ans[3]
mValue=mValu[0]
print mValue
if((mValue >= 0.180) and (mValue < 0.210)):
    print "Semicircle"



cv2.waitKey(0)
cv2.destroyAllWindows()

