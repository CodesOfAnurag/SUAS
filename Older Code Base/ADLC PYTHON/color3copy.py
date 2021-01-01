import cv2
import numpy as np
def kmeans(image):
    #image=cv2.GaussianBlur(image,(7,7),0)
    vectorized=image.reshape(-1,3)
    vectorized=np.float32(vectorized) 
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans (vectorized,3,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    res = center[label.flatten()]
    segmented_image = res.reshape((image.shape))
    return label.reshape((image.shape[0],image.shape[1])),segmented_image.astype(np.uint8)

def extractComponent(image,label_image,label):
    component=np.zeros(image.shape,np.uint8)
    component[label_image==label]=image[label_image==label]
    return component

image=cv2.imread("/home/manohar/Outputs/Targets/m-0.PNG",1)
label,result=kmeans(image)
print "end"
cv2.imshow("clustered",result)
result0=extractComponent(image,label,0)
result1=extractComponent(image,label,1)
result2=extractComponent(image,label,2)
cv2.imshow("cluster0",result0)
cv2.imshow("cluster1",result1)
cv2.imshow("cluster2",result2)

cv2.waitKey(0)
cv2.destroyAllWindows()
