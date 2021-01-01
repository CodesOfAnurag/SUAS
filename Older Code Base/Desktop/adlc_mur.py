from Tkinter import *
from PIL import Image, ImageTk
from ttk import *
import glob
import os
import os.path
import time
import subprocess 
import pyinotify

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)

global a
a=1

## Main window
root = Tk()
## Grid sizing behavior in window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
## Canvas
cnv = Canvas(root)
cnv.grid(row=0, column=0, sticky='nswe')
## Scrollbars for canvas
hScroll = Scrollbar(root, orient=HORIZONTAL, command=cnv.xview)
hScroll.grid(row=1, column=0, sticky='we')
vScroll = Scrollbar(root, orient=VERTICAL, command=cnv.yview)
vScroll.grid(row=0, column=1, sticky='ns')
cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
## Frame in canvas
frm = Frame(cnv)
## This puts the frame in the canvas's scrollable zone
cnv.create_window(0, 0, window=frm, anchor='nw')



while True:
    
    def det():
        print('umm')
        global a
        while os.path.exists("/home/sush/Detected/Target%d.jpg" % a):
            print('ok')
            ## Frame contents
            list2 = glob.glob("/home/sush/Detected/*.jpg")
            list3 = glob.glob("/home/sush/Detected/*.txt")
            y = 0
            for x in list2:
                y = y + 1
                lbl = Label(frm, text="Target %s" % y)
                lbl.pack(side=TOP, padx=10, pady=30)
                T = Text(frm, height=10, width=50)
                background = Label(frm)
                try:
                    f = open(list3[y - 1])
                    data = f.read()
                    T.insert(END, data)
                    f.close()
                    image = Image.open(x)
                    background_image = ImageTk.PhotoImage(image)
                    background.configure(image=background_image)
                    background.image = background_image

                except IOError as e:
                    print('Not yet detected')
                    background.configure(text="Target yet to be detected")
                background.pack(padx=10, pady=10)
                T.pack(side=TOP, padx=10, pady=10)
            send = send = Button(root, text="Send")
            send.grid(row=50, column=0)
            a=a+1

            def Send(self):
                os.system('python qwerty.py')
            send.bind("<Button-1>", Send)
    
    ## Update display to get correct dimensions
    frm.update_idletasks()
    ## Configure size of canvas's scrollable zone
    cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
    ## Go!
    root.mainloop() 
    det()


