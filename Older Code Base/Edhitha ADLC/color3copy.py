import cv2
import numpy as np
def kmeans(image):
    #image=cv2.GaussianBlur(image,(7,7),0)
    vectorized=image.reshape(-1,3)
    vectorized=np.float32(vectorized) 
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans (vectorized,3,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    res = center[label.flatten()]
    segmented_image = res.reshape((image.shape))
    return label.reshape((image.shape[0],image.shape[1])),segmented_image.astype(np.uint8)

def extractComponent(image,label_image,label):
    component=np.zeros(image.shape,np.uint8)
    component[label_image==label]=image[label_image==label]
    return component

#def detect(cluster):


################################################################################
image=cv2.imread("Semicircle.PNG",1)
cv2.imshow("original",image)
label,result=kmeans(image)
print "end"
cv2.imshow("clustered",result)
result0=extractComponent(result,label,0)
result1=extractComponent(result,label,1)
result2=extractComponent(result,label,2)
cv2.imshow("cluster0",result0)
cv2.imshow("cluster1",result1)
cv2.imshow("cluster2",result2)
###############################################################################
blurred = cv2.GaussianBlur(result0,(5,5),0)
cv2.imshow("smooth",blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
