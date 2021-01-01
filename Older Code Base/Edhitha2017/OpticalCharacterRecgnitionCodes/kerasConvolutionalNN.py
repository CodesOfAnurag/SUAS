from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import model_from_json
import os
import numpy as np
import cv2
import h5py
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils

from keras import backend as K
K.set_image_dim_ordering('th')

di = '/media/niran/New Volume/DatabaseOCRShuffled/'

l = 1

#Function to return images and corresponding one hot vectors of the given index as a batch

def getNextBatch(num, i):
    batch_xs1 = []
    batch_ys1 = []
    imageList = []
    oh = []
    # j = randint(0,5)
    #Reading from memmaps
    fp1 = np.memmap(di + 'InputOCR' + str(i) + '.dat', dtype='float32', mode='r', shape=(1800, 64, 64, 1))
    imageList[:] = fp1[:]
    ohv1 = np.memmap(di + 'TargetOCRVectors' + str(i) + '.dat', dtype='float32', mode='r', shape=(1800, 36))
    oh[:] = ohv1[:]
    
    #return 4 out of every 5 images to keep those images reserved for validation
    for p in range(num):
        # k = randint(1,1000)
        if(p%5!=0):
            img = np.reshape(imageList[p], (1, 64, 64))
            batch_xs1.append(img)
            batch_ys1.append(oh[p])
    batch_xs1 = np.asarray(batch_xs1)
    batch_ys1 = np.asarray(batch_ys1)
    return batch_xs1, batch_ys1
    
#Function to return validation images
def testImagesDefine():
    batch_xs2 = []
    batch_ys2 = []
    imageList = []
    oh = []
    for j in range(0, 20):
        fp1 = np.memmap(di + 'InputOCR' + str(j) + '.dat', dtype='float32', mode='r', shape=(1800, 64, 64, 1))
        imageList[:] = fp1[:]
        ohv1 = np.memmap(di + 'TargetOCRVectors' + str(j) + '.dat', dtype='float32', mode='r', shape=(1800, 36))
        oh[:] = ohv1[:]
        for i in range(0, 1800):
            # k = randint(300,310)
            #return one in five images as a validation image
            if (i%5==0) :
                img = np.reshape(imageList[i], (1, 64, 64))
                batch_xs2.append(img)
                batch_ys2.append(oh[i])
    batch_xs2 = np.asarray(batch_xs2)
    batch_ys2 = np.asarray(batch_ys2)
    return batch_xs2, batch_ys2    
    
l = 1

#The convolution neural network model
if l==0:
    model = Sequential()
    model.add(Convolution2D(16, 5, 5, input_shape=(1, 64, 64), activation='relu', border_mode='same'))
    model.add(Convolution2D(16, 5, 5, activation='relu', border_mode='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(32, 5, 5, activation='relu', border_mode='same'))
    model.add(Convolution2D(32, 5, 5, activation='relu', border_mode='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(64, 5, 5, activation='relu', border_mode='same'))
    model.add(Convolution2D(64, 5, 5, activation='relu', border_mode='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(1024,activation='relu'))
    model.add(Dense(36, activation='softmax'))

    # Compile model

    #epochs = 25
    #lrate = 0.01
    #decay = lrate/epochs
    #sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())  
else:
	#Load an appropriate a model instead of defining it again
    json_file = open('/media/niran/New Volume/ModelsAndWeights3/ModelConvolution49.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("/media/niran/New Volume/ModelsAndWeights3/ModelConv49.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
X_test, Y_test = testImagesDefine()
#X_pred, Y_pred = predictImagesDefine()
loss = 0.0
acc = 0.0

losses = []
accuracies = []
valLosses = []
valAccuracies = []

lossAndAccuracy = {}
valLossAndAccuracy = {}

thefile = open('LOSSESFTWO.txt', 'a')
thefile2 = open('ACCURACIESFTWO.txt', 'a')
thefile3 = open('VALIDATIONLOSSESFTWO.txt', 'a')
thefile4 = open('VALIDATIONACCURACIESFTWO.txt', 'a')

for epoch in range(50, 60):
    loss = 0.0
    acc = 0.0
    print ("Epoch: " + str(epoch))
    for i in range(0,20):
        print ("Index: " + str(i))
        X_batch, Y_batch = getNextBatch(1800,i)
        hist = model.fit(X_batch, Y_batch, nb_epoch=1, batch_size=32)
        l = hist.history.values()[1]
        a = hist.history.values()[0]
        loss += float(l[0])
        acc += float(a[0])

    avgLoss = loss/(i+1)
    avgAcc = acc/(i+1)
    print ("For training: ")
    print avgLoss
    print  avgAcc
    losses.append(avgLoss)
    accuracies.append(avgAcc)
    LandA = (avgLoss, avgAcc)
    lossAndAccuracy[epoch] = LandA

    thefile.write("%f\n" % avgLoss)
    thefile2.write("%f\n" % avgAcc)

    loss_and_metrics = model.evaluate(X_test, Y_test, batch_size=32)
    print ("For validaion: ")
    print loss_and_metrics[0]
    print loss_and_metrics[1]
    valLosses.append(loss_and_metrics[0])
    valAccuracies.append(loss_and_metrics[1])
    valLossAndAccuracy[epoch] = (loss_and_metrics[0], loss_and_metrics[1])

    thefile3.write("%f\n" % loss_and_metrics[0])
    thefile4.write("%f\n" % loss_and_metrics[1])

    model_json = model.to_json()
    with open("/media/niran/New Volume/ModelsAndWeights3/ModelConvolution" + str(epoch) + ".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("/media/niran/New Volume/ModelsAndWeights3/ModelConv" + str(epoch) + ".h5")
    print("Saved model" + str(epoch) + " to disk")

thefile.close()
thefile2.close()
thefile3.close()
thefile4.close()

print "LOSSES: "
print losses

print "ACCURACIES: "
print accuracies

print "BOTH: "
print lossAndAccuracy


#Training results saving

with open("LOSSESANDACCURACIESFTWO", 'a') as f:
    json.dump(lossAndAccuracy, f)

#Validation results saving

with open("VALIDATIONLOSSESANDACCURACIESFTWO", 'a') as f:
    json.dump(valLossAndAccuracy, f)
