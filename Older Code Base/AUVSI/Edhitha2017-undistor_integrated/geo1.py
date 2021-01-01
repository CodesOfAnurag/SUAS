from geographiclib.geodesic import Geodesic
import math
import pyexiv2

x = 1185   #second value in pixel location
y = 1244   #first value in pixel location

metadata = pyexiv2.ImageMetadata("/home/roopak/Desktop/22.jpg")   #insert image address
metadata.read()
tag1 = metadata['Exif.Image.Orientation']
tag2 = metadata['Exif.Photo.UserComment']
data = tag2.value.split(' ')

lat = float(data[0])
lon = float(data[1])
alt = float(data[2])
orientation = float(data[3])
ortag = 0

print data[0]
if tag1.value==3:
	print "Orientation add  180"
	ortag = 0
elif tag1.value==8:
	print "Orientation add  90"
	orientation = orientation + 90
        ortag = 1
elif tag1.value==6:
	print "Orientation sub 90"
	orientation = orientation - 90	
	ortag = 1		
else:
	ortag = 0


if(ortag == 1):
	print "potrait"
	imgHeight = (2 * alt * math.tan(21.8*3.1415/180))/6000;
	imgWidth  = (2 * alt * math.tan(14.95*3.1415/180))/4000;
	xo=2000
	yo=-3000

	x1 = xc * imgWidth
	y1 = y * -1 * imgHeight

	xo = xo * imgWidth
	yo = yo * imgHeight 

	d = math.sqrt(((y1-yo)*(y1-yo))+((x1-xo)*(x1-xo)))
	print("distance of target from centre  : ",d)

	angle = abs((yo-y1)/(xo-x1))	
	target_angle = abs(math.degrees(math.atan(angle)))
	print target_angle

	if(y<3000 and x>2000):
		print "1st quadrant"
		target_orientation  = orientation + target_angle  
	elif(y<3000 and x<2000):
		print "2nd quadrant"
		target_orientation  = orientation - ( 90 - target_angle )

	elif(y>3000 and x<2000):
		print "3rd quadrant"
		target_orientation  = orientation - ( 90 + target_angle )  

	elif(y>3000 and x>2000):
		print "4th quadrant"
		target_orientation  = orientation + 90 + target_angle

if(ortag == 0):
	print "Landscape"
	imgHeight = (2 * alt * math.tan(14.95*3.1415/180))/4000;
	imgWidth  = (2 * alt * math.tan(21.8*3.1415/180))/6000;
	xo=3000
	yo=-2000

	x1 = x * imgWidth
	y1 = y * -1 * imgHeight

	xo = xo * imgWidth
	yo = yo * imgHeight 

	d = math.sqrt(((y1-yo)*(y1-yo))+((x1-xo)*(x1-xo)))
	print("distance of target from centre : ",d)

	angle = abs((yo-y1)/(xo-x1))	
	target_angle = abs(math.degrees(math.atan(angle)))
	print target_angle

	if(y<2000 and x>3000):
		print "1st quadrant"
		target_orientation  = orientation + target_angle  
	elif(y<2000 and x<3000):
		print "2nd quadrant"
		target_orientation  = orientation - ( 90 - target_angle )
	elif(y>2000 and x<3000):
		print "3rd quadrant"
		target_orientation  = orientation - ( 90 + target_angle )  
	elif(y>2000 and x>3000):
		print "4th quadrant"
		target_orientation  = orientation + 90 + target_angle

if(target_orientation > 360):
	target_orientation = target_orientation -360

if(target_orientation < 0):
	target_orientation = target_orientation + 360


print("target_orientation with respect to centre : " ,target_orientation)

geod = Geodesic.WGS84 
g = geod.Direct(lat, lon, target_orientation,d)
print("Target latitude is ",g['lat2'],"       ", "Target longitude is ", g['lon2'] )


latOri = 13.23532 #enter actual location of target for verificattion
lonOri = 77.3255
g = geod.Inverse(latOri, lonOri, g['lat2'], g['lon2'])
print "The Accuracy of geolocation is {:.3f} m.".format(g['s12'])






