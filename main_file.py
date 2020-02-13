from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time 
import mser
import color_and_char_extraction
import shape
import threading
import cv2
import write_json

countImg, c, countCrop, ci = 0,0,0,0

#path of the incoming images folder
img_cap_path = '/home/cz/Desktop/test_codes/test_folder'

#path of images write folder
img_write_path = "/home/cz/Desktop/test_codes/test_folder2"

img_list=list()
crop_img_list=[]

#mser
def mser():
	global countImg,crop_img_list
	while True:
		try :
			print(img_list[countImg])
			lists = mser2.execute(img_list[countImg])
			crop_img_list = crop_img_list + lists
			print "crop_img_list = ",len(crop_img_list)
			countImg+=1
		except IndexError :
			continue

# this function provides cropped images for detection
def provide_cropped_img():
	global countCrop,ci
	if(countCrop<len(crop_img_list)):
		img = crop_img_list[countCrop]
		ci = len(crop_img_list)
		lol = 1
		countCrop+=1
		return img,countCrop-1,lol;
	else:
		return 0,0,0;

#For color, shape, char detection
def odlc_detect():
	while(True):
		img,c,lol = provide_cropped_img()
		if(c<ci and lol):
				shape = shape_detection.execute(img)
				bg,lt,ext = color_and_char_extraction.execute(img)
				lol=0	
				if(bg!=lt and lt and bg):
					print "\nNew Target Detected"
					features = dict()
					features["shape"] = shape
					features["background_color"] = bg
					features["alphanumeric"] = "s"
					features["alphanumeric_color"] = lt
					features["orientation"] = "east"
					write_json.writeToJSONfile(img_write_path,features,img)
					

#watcher script to detect incomming images
class MyHandler(PatternMatchingEventHandler):
	patterns = ["*.JPG", "*.JPEG",".jpg",".png",".JPG"]
	global img_list    
	def process(self, event):
		name = event.src_path.split('\\')[::-1]
		name = name[0]
		#name = name[:-7]
		print(name)
		img_list.append(name)
		
	

	def on_created(self, event):
		self.process(event)

	#def on_moved(self, event):
	#	print("moved")
	#	self.process(event)
		

def start_observe(path):

    observer = Observer()
    observer.schedule(MyHandler(), path=path)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# 1 thread of watcher script;  1 thread of mser;  3 thread of odlc_detection
t1 = threading.Thread(target=start_observe, args=(img_cap_path,))
t2 = threading.Thread(target=mser, args=())
t3 = threading.Thread(target=odlc_detect, args=())
t4 = threading.Thread(target=odlc_detect, args=())
t5 = threading.Thread(target=odlc_detect, args=())

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()


