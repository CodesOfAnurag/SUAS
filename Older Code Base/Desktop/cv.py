import cv2

img = cv2.imread("/home/manohar/23may/flt1/capt0033.jpg",1)
cv2.imshow("FML",img)
cv2.waitKey()
cv2.destroyAllWindows()
