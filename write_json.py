import json
import cv2
file_number = 0
def writeToJSONfile(path,features,img):
	global file_number
	filename = "%d"%file_number
	file_path_name_with_ext = path + '/' + filename	+ '.json'
	with open(file_path_name_with_ext,'w') as fp:
		json.dump(features,fp)
	
	img_name = path + '/' + filename + '.png'
	cv2.imwrite(img_name,img)
	file_number += 1

