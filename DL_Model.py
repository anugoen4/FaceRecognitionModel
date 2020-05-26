# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:01:31 2019

@author: Spectre
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 00:19:35 2019

@author: Spectre
"""
import numpy as np

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Flatten, Dense,Dropout

classifier = Sequential()

#Step -1 Adding First Convolution Layer 
classifier.add(Convolution2D(32,3,3,input_shape = (32,32,3),activation = 'relu'))

#Step -2 Max Pooling
classifier.add(MaxPooling2D(pool_size = (2,2)))


#Adding second convolution layer (optional)
classifier.add(Convolution2D(32,2,2,activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))

#Step -3 Flattening
classifier.add(Flatten())

#Step -4 Full Connection
classifier.add(Dense(output_dim = 128,activation = 'relu'))
classifier.add(Dense(output_dim = 128,activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(output_dim = 128,activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(output_dim = 128,activation = 'relu'))
classifier.add(Dense(output_dim = 128,activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(output_dim = 64,activation = 'relu'))
classifier.add(Dense(output_dim = 1,activation = 'sigmoid'))


#Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


train_datagen = ImageDataGenerator(rescale = 1./255,shear_range = 0.2,zoom_range = 0.2,horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(
        'dataset_2/training_set',target_size = (32,32),batch_size = 32,class_mode = 'binary')
test_set = test_datagen.flow_from_directory(
        'dataset_2/test_set',target_size = (32,32),batch_size = 32,class_mode = 'binary')

classifier.fit_generator(
        training_set,steps_per_epoch = 1600,nb_epoch = 50,validation_data = test_set,nb_val_samples = 400)

model_json = classifier.to_json()
with open("model_gray.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("model_gray.h5")
