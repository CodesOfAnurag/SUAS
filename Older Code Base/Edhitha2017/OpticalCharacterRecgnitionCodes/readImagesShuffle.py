import numpy as np
import random
direc = '/media/niran/New Volume/DatabaseOCRShuffled/'
di = '/media/niran/New Volume/DatabaseOCR/'

for num in range(0,1000,50):
    imageList = []
    oh = []
    a = []
    b = []
    for j in range(0,36):
        print j
        fp1 = np.memmap(di + 'InputOCR' + str(j + 1) + '.dat', dtype='float32', mode='r', shape=(1016, 64, 64, 1))
        a = fp1[num:num+50]
        ohv1 = np.memmap(di + 'TargetOCRVectors' + str(j + 1) + '.dat', dtype='float32', mode='r', shape=(1016, 36))
        b = ohv1[num:num+50]
        
        c = list(zip(a,b))
        random.shuffle(c)
        a,b = zip(*c)

        imageList += a
        oh += b

    print len(imageList)
    
    fp2 = np.memmap(direc + 'InputOCR' + str(num/50) + '.dat', dtype='float32', mode='w+', shape=(len(imageList), 64, 64, 1))
    fp2[:] = imageList[:]
    ohv2 = np.memmap(direc + 'TargetOCRVectors' + str(num/50) + '.dat', dtype='float32', mode='w+', shape=(len(oh), 36))
    ohv2[:] = oh[:]
