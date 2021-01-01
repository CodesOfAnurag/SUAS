import sys
import time
import pyexiv2
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

'''
Extend FileSystemEventHandler to be able to write custom on_any_event method
'''
class MyHandler(FileSystemEventHandler):
    '''
    Overwrite the methods for creation, deletion, modification, and moving
    to get more information as to what is happening on output
    '''
    def on_created(self, event):
        filepath=event.src_path
	print filepath
	metadata = pyexiv2.ImageMetadata(filepath)
	metadata.read()
	tag1 = metadata['Exif.Image.Orientation']
	#print tag1[34]
	print tag1.value
	if tag1.value==3:
		img = Image.open(filepath)
		img2 = img.rotate(180,expand=1)
		img2.save(filepath)
	elif tag1.value==8:
		img = Image.open(filepath)
		img2 = img.rotate(-90,expand=1)
		img2.save(filepath)
		print "llol"
	elif tag1.value==6:
		img = Image.open(filepath)
		img2 = img.rotate(90,expand=1)
		img2.save(filepath)					
	else:
		print "beti"
watch_directory ="/home/aditya/Untitled Folder"# sys.argv[1]       # Get watch_directory parameter

event_handler = MyHandler()

observer = Observer()
observer.schedule(event_handler, watch_directory, True)
observer.start()

'''
Keep the script running or else python closes without stopping the observer
thread and this causes an error.
'''
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
