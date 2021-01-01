import cv2
import numpy as np






def create_blank(width, height, rgb_color=(0, 0, 0,0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


#def enlargeROI(img,box,padding):
   # returnrect=





# Create new blank 300x300 red image
width, height = 300, 300
img=cv2.imread("D.JPG",1)


img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

avg_col= cv2.mean(img_hsv)

print avg_col
red = (255, 0, 0)


image = create_blank(np.size(img,1),np.size(img,0), rgb_color=(avg_col[0],avg_col[1],avg_col[2]))
#cv2.imwrite('red.jpg', image)

final = cv2.subtract(img_hsv,image)
BGR = cv2.cvtColor(final,cv2.COLOR_HSV2BGR)
final = cv2.cvtColor(BGR,cv2.COLOR_BGR2GRAY)
#cv2.imshow("lol",final)


##rop_img = img[200:350,450:700]
##cv2.imshow("crops",rop_img)

mser = cv2.MSER(5,100, 7000, 0.1, 0.2, 200, 1.01, 0.002, 5)
bboxes = mser.detect(final)

cv2.imshow("constant",bboxes[56])

constant= cv2.copyMakeBorder(bboxes[25],10,10,10,10,cv2.BORDER_CONSTANT)
#res = cv2.resize(constant,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#cv2.imshow("constant",constant)

avg = len(bboxes)
print avg



##for box in bboxes :
##    b=box[len(box)-1]
##    a=box[0]
##    if ((abs(a[0]-b[0])>5) and (abs(a[1]-b[1])>5)):
##        print "entered loop"
##        crop_img = img[a[0]:b[0],a[1]:b[1]]
##        res = cv2.resize(crop_img,None,fx=12, fy=12, interpolation = cv2.INTER_CUBIC)
##        cv2.imshow('bbox.PNG',res)
##        cv2.waitKey(0)
##    print a[0]
##    print b[0]
##    print a[1]
##    print b[1]
##    print "###########################################################"

#cv2.imshow("crop",crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
