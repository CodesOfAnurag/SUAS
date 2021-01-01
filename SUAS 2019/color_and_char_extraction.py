#-------The following program finds color of letter and background from cropped image and extraction of letter for OCR---------# 
#packages required - opencv 3.206 , numpy
import cv2
import numpy as np

def execute(img):
	#read Cropped image and convert to LAB Colorspace
	image=img
	img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	reshaped = img.reshape((-1,3))
	#apply k-means
	reshaped = np.float32(reshaped)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 2.0)
	ret,label,center=cv2.kmeans(reshaped,3,None,criteria,30,cv2.KMEANS_RANDOM_CENTERS)

	#color detection
	bl = (int(round(center[1,0])))
	ba = (int(round(center[1,1])))
	bb = (int(round(center[1,2])))
	ll = (int(round(center[2,0])))
	la = (int(round(center[2,1])))
	lb = (int(round(center[2,2])))

	#function to convert LAB to HSV Colorspace 
	def convrt(l,a,b):
		img = np.uint8([[[l,a,b]]])
		img = cv2.cvtColor(img,cv2.COLOR_Lab2RGB)
		img = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)	
		l = (img[0][0][0])
		a = (img[0][0][1])
		b = (img[0][0][2])
		l = l*2
		a = (a * 100) / 255
		b = (b * 100) / 255
		return l,a,b

	#function to Compare obtained HSV values with standard HSV values
	def compa(h,s,v):
		if( s==0 or (s>0 and s<8)):
			return "white"
			exit()
		elif(v==0 or (v>0 and v<18)):
			return "black"
			exit()
		elif((h>335 and h<360) or (h>0 and h<15)):
			return "red"
			exit()
		elif(h>180 and h<260):
			return "blue"
			exit()
		elif(h>75 and h<145):
			return "green"
			exit()
		elif(h>40 and h<65):
			return "yellow"
			exit()
		elif(h>270 and h<305):
			return "purple"
			exit()
		elif(h>18 and h<28):
			return "orange"
			exit()
		else:
			return False

	#char extraction
	def ext(reshaped,label,center,image):
		res = center[label.flatten()]
		x = len(reshaped[label.ravel()==0])#number of cluster points in the first cluster
		y = len(reshaped[label.ravel()==1])#number of cluster points in the second cluster
		z = len(reshaped[label.ravel()==2])#number of cluster points in the third cluster 

		#getting the smallest cluster, smallest cluster=character cluster
		minCluster = min(x,y,z)
		reshaped = res.reshape((image.shape))#reshaping center[label]
		label = label.reshape((image.shape[0],image.shape[1]))
		smooth= reshaped.astype(np.uint8)#converting to image

		#function which returns a cluster's points as in the image
		def labler(image,label_image,label):
			component=np.zeros(image.shape,np.uint8)
			component[label_image==label]=image[label_image==label]
			return component

		if x==minCluster: #if x is the smallest cluster then mask out x and print masked image 
			cluster=labler(smooth,label,0)
			thinned = np.ones((5,5),np.uint8)
			thinned = cv2.erode(cluster,thinned,iterations=1)
			return thinned

		elif y==minCluster: #if y is the smallest cluster then mask out y and print masked image 
			cluster=labler(smooth,label,1)
			thinned = np.ones((5,5),np.uint8)
			thinned = cv2.erode(cluster,thinned,iterations=1)
			return thinned
		
		else:   #elsez must be the smallest cluster thne mask out z and print masked image 
			cluster=labler(smooth,label,2)
			thinned = np.ones((5,5),np.uint8)
			thinned = cv2.erode(cluster,thinned,iterations=1)
			return thinned
	

	h,s,v = convrt(bl,ba,bb)
	bg = compa(h,s,v)
	h,s,v = convrt(ll,la,lb)
	lt = compa(h,s,v)
	ext = ext(reshaped,label,center,image)
	return bg,lt,ext
	
