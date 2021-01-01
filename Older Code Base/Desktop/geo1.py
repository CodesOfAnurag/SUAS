from geographiclib.geodesic import Geodesic
import math
import pyexiv2

#exifdata  = #get exif from string.pls fill in code 
#data  =  exifdata.split()

lat = 13.1507649
lon = 77.4840584
alt = 975.07-861
orientation = 36.18
ortag = 0

x = 3040 #second value in pixel location
y = 1100   #first value in pixel location

metadata = pyexiv2.ImageMetadata("/home/manohar/Geotagged/22.jpg")
metadata.read()
tag1 = metadata['Exif.Image.Orientation']

print tag1.value

if tag1.value==3:
	#img2 = img.rotate(180,expand=1)
	print "Orientation add  180"
	orientation = orientation + 180
	ortag = 0
elif tag1.value==8:
	#img2 = img.rotate(-90,expand=1)#clockwise
	print "Orientation add  90"
	orientation = orientation + 90
        ortag = 1
elif tag1.value==6:
	#img2 = img.rotate(90,expand=1)#anticlockwise
	print "Orientation sub 90"
	orientation = orientation - 90	
	ortag = 1		
else:
	ortag = 0

if(ortag == 1):
	print "tilt"
	imgHeight = (2*alt * math.tan((21.8*3.141592653589793)/180))/6000;
	imgWidth  = (2*alt * math.tan((14.95*3.141592653589793)/180))/4000;
	xo=2000
	yo=3000

	x1 = x * imgWidth
	y1 = y * imgHeight

	xo = xo * imgWidth
	yo = yo * imgHeight

	d = math.sqrt(((y1-yo)*(y1-yo))+((x1-xo)*(x1-xo)))
	print("distance is : ",d)
	if(y<3000 and x>2000):
		print "1st quadrant"
		angle = abs((x-2000.0)/(3000.0-y))
		 #m= (y-2000)/(x-3000)	
		target_angle = math.degrees(math.atan(angle))
		target_orientation  = orientation - target_angle  

	elif(y<3000 and x<2000):
		print "2nd quadrant"
		angle = abs((2000.0-x)/(3000.0-y))
		target_angle = math.degrees(math.atan(angle))
		target_orientation  = orientation + target_angle

	elif(y>3000 and x<2000):
		print "3rd quadrant"
		angle =(y-3000.0)/(2000.0-x)
		target_angle = 270 - math.degrees(math.atan(angle))
		target_orientation  = orientation - (target_angle)

	elif(y>3000 and x>2000):
		print "4th quadrant"
		angle =(y-3000.0)/(x-2000.0)
		target_angle = 90 + math.degrees(math.atan(angle))
		target_orientation  = orientation - (target_angle)

if(ortag == 0):
	imgHeight = (2 * alt * math.tan(14.95))/4000;
	imgWidth  = (2 * alt * math.tan(21.8))/6000;
	xo=3000
	yo=2000

	x = x * imgWidth
	y = y * imgHeight

	xo = xo * imgWidth
	yo = yo * imgHeight

	d = math.sqrt(((y-yo)*(y-yo))+((x-xo)*(x-xo)))
	print("distance is : ",d)
	if(y<2000 and x>3000):
		print "1st quadrant"
		angle = abs((x-3000.0)/(2000.0-y))
		 #m= (y-2000)/(x-3000)	
		target_angle = math.degrees(math.atan(angle))
		target_orientation  = orientation - target_angle  

	if(y<2000 and x<3000):
		print "2nd quadrant"
		angle = abs((3000.0-x)/(2000.0-y))
		target_angle = math.degrees(math.atan(angle))
		target_orientation  = orientation + target_angle

	if(y>2000 and x<3000):
		print "3rd quadrant"
		angle =(y-2000.0)/(3000.0-x)
		target_angle = 270 - math.degrees(math.atan(angle))
		target_orientation  = orientation - (target_angle)

	if(y>2000 and x>3000):
		print "4th quadrant"
		angle =(y-2000.0)/(x-3000.0)
		target_angle = 90 + math.degrees(math.atan(angle))
		target_orientation  = orientation - (target_angle)

if(target_orientation > 360):
	target_orientation = target_orientation -360

if(target_orientation < 0):
	target_orientation = target_orientation + 360

#print(target_orientation)
#print(alt)
#d=d*imgHeight
#target_orientation = 260
geod = Geodesic.WGS84 
g = geod.Direct(lat, lon, target_orientation,d)
print(g['lat2'],g['lon2'])
