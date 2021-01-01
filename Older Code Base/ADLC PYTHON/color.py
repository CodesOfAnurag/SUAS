import numpy as np
import cv2

img = cv2.imread("/home/manohar/Outputs/Targets/m-0.PNG",1)
cv2.imshow("original",img)

Z = img.reshape((-1,3))

Z = np.float32(Z)


# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

K = 3
attempts=10
ret,label,center=cv2.kmeans(Z,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
component=np.zeros(img.shape,np.uint8)
component[label_img==label]=img[label_img==label]
#res2 is the result of the frame which has undergone k-means clustering

cv2.imshow("segmented",center)
result=extractComponent(img,label,0)
cv2.imshow("extracted",result)
cv2.waitKey()
cv2.destroyAllWindows()
