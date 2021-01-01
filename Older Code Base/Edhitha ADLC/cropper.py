import cv2
import numpy as np

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect
	
def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
	# return the warped image
	return warped

def skeletonise(img):
	#img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	size = np.size(img)
	Single_Line = np.zeros(img.shape,np.uint8)
	 
	ret,img = cv2.threshold(img,127,255,0)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	Done_Flag=0

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

	return Single_Line

def crop_transform_pad(image):
	imagehsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

	lower_blue = np.array([10,10,2])
	upper_blue = np.array([255,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(imagehsv, lower_blue, upper_blue)	
	#cv2.imshow("mask",mask)
	imagec,cnts, _ = cv2.findContours(mask.copy(), cv2. RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#print("contours = ",len(cnts))		
	for c in cnts:
		#cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		#(x,y,w,h) = cv2.boundingRect(c)
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		#cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
		#hull = cv2.convexHull(c)
		#cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

	#print(box)
	#cropped = image[y:y+h, x:x+w]
	#[(73, 239), (356, 117), (475, 265), (187, 443)]
	pts = [(box[0][0], box[0][1]), (box[1][0],box[1][1]), (box[2][0], box[2][1]), (box[3][0],box[3][1])]
	pts = np.array(pts, dtype = "float32")
	warped = four_point_transform(mask, pts)
	#cv2.imshow("Outline",image)
	#cv2.imshow("warped",warped)
	#res = cv2.resize(warped,(100,100))
	bordersize=10
	border = cv2.copyMakeBorder(warped, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
	
	return warped


image = cv2.imread('I.PNG',1)

cropped = crop_transform_pad(image)
cv2.imshow("crop",cropped)
#single_line = skeletonise(cropped)
#cv2.imshow("final",single_line)
cv2.waitKey(0)
cv2.destroyAllWindows()
