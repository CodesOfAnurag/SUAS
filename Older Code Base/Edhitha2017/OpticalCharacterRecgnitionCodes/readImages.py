import os
import cv2
import glob
import numpy as np

def oneHotGenerator(num):
	temp = np.zeros(36)
	temp[num]=1
	
	return temp
	
i=0
w = 5080

for directory in os.listdir('/media/niran/New Volume/OCR'):
	
	imageList=[]
	OneHotVectorList=[]
	print('/media/niran/New Volume/OCR/'+directory)
	i=int(directory[1:])
	print(i)
	if int(i) < 37:
		oneHotVector = oneHotGenerator(int(i)-1)

		print(oneHotVector)

		os.chdir('/media/niran/New Volume/OCR/'+directory)
		j=0
		for filename in glob.glob("*.png"):

			OneHotVectorList.append(oneHotVector)

			img = cv2.imread(filename)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = cv2.resize(img, (64,64))
			img = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
			img = np.reshape(img, (64,64,1))

			imageList.append(img)
			j=j+1

			print(filename)	
		fp1 = np.memmap('/media/niran/New Volume/DatabaseOCR/InputOCR'+str(i)+'.dat', dtype = 'float32', mode = 'w+', shape = (j,64,64,1))
		fp1[:] = imageList[:]
		ohv1 = np.memmap('/media/niran/New Volume/DatabaseOCR/TargetOCRVectors'+str(i)+'.dat', dtype = 'float32', mode = 'w+', shape = (j,36))
		ohv1[:] = OneHotVectorList[:]
