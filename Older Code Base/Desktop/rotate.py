import cv2

image = cv2.imread("/home/manohar/Desktop/capt0029.jpg",1)

(h, w) = image.shape[:2]
center = (6000, 4000)
center2 = (center[1],center[0])
print center[1]
print center[0]

# rotate the image by 180 degrees
M = cv2.getRotationMatrix2D(center, 180, 1.0)

rotated = cv2.warpAffine(image, M, (6000,4000))

cv2.imshow("rotated", rotated)
cv2.imwrite("rotated.JPG",rotated)
cv2.waitKey(0)
