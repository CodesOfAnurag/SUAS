import cv2
import numpy as np
from operator import xor

def execute(cap_img):
	print "new img = ",cap_img
	def create_blank(width, height, rgb_color=(0, 0, 0,0)):
		"""Create new image(numpy array) filled with certain color in RGB"""
		# Create black blank imag
		image = np.zeros((height, width, 3), np.uint8)
		# Since OpenCV uses BGR, convert the color first
		color = tuple(reversed(rgb_color))
		# Fill image with color
		image[:] = color
		return image

	#program start , read image
	width, height = 300, 300
	img=cv2.imread(cap_img,1)
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#cal mean_color of image and create image of same color
	avg_col= cv2.mean(img_hsv)
	image = create_blank(np.size(img,1),np.size(img,0), rgb_color=(avg_col[0],avg_col[1],avg_col[2]))
	image2 = create_blank(np.size(img,1),np.size(img,0), rgb_color=(avg_col[2],avg_col[1],avg_col[0]))

	finala = cv2.subtract(img_hsv,image)
	final = cv2.subtract(finala,image2)

	BGR = cv2.cvtColor(final,cv2.COLOR_HSV2BGR)
	final = cv2.cvtColor(BGR,cv2.COLOR_BGR2GRAY)

	#### BEGIN MSER ####
	gray = final
	delta = 3
	min_area=400
	max_area = 3800
	max_variation = 0.16
	padding = 10
	mser = cv2.MSER_create(delta, min_area, max_area, max_variation, 0.2, 200, 1.01, 0.002, 5)

	regions, bboxes = mser.detectRegions(gray) # *** Edited for crops ***
	vis = img.copy()


	hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

	cv2.polylines(vis, hulls, 1, (0, 255, 0))

	mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)

	for contour in hulls:

		cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

	#this is used to find only text regions, remaining are ignored
	detected = cv2.bitwise_and(img, img, mask=mask)
	####CROP PART####

	crops = []
	xref , yref = 1000000, 1000000

	for i in range(len(bboxes)):
		x,y,w,h = bboxes[i]
		if abs(x-xref)>10 and abs(y-yref)>10 and not (w>150 or h>150):
		    if (x < padding or y < padding):
		        crops.append(detected[y:y+h+padding,x:x+padding+w])
		    else:
		        crops.append(detected[y-padding:y+h+padding,x-padding:x+padding+w])
		xref = x
		yref = y
	return crops

