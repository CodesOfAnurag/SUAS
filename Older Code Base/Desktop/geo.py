from geographiclib.geodesic import Geodesic
import math


#exifdata  = #get exif from string.pls fill in code 
#data  =  exifdata.split()

lat = 13.1499844
lon = 77.4834351
alt = 957.97-861
orientation = 167.01-90


x = 210  #second value in pixel location
y = 3069   #first value in pixel location





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

imgHeight = (2 * alt * math.tan(14.95))/4000;
imgWidth  = (2 * alt * math.tan(21.8))/6000;

print(target_orientation)
print(alt)
#d=d*imgHeight


x = 3487  #second value in pixel location
y = 2301   #first value in pixel location
xo=3000
yo=2000

x = x * imgWidth
y = y * imgHeight

xo = xo * imgWidth
yo = yo * imgHeight

d = math.sqrt(((y-yo)*(y-yo))+((x-xo)*(x-xo)))
print d
#target_orientation = 260
geod = Geodesic.WGS84 
g = geod.Direct(lat, lon, target_orientation,d)
print(g['lat2'],g['lon2'])
