import os,sys
folder = '/home/manohar/2016 Aerial images/SUAS 2016 pictures (2)/suas-images/'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.JPG', '.jpg')
       output = os.rename(infilename, newname)
