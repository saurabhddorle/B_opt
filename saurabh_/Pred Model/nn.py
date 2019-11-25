# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:49:10 2019

@author: sdorle
"""

# # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline


# # Importing Dataset
dataset = pd.read_csv("data\\Train_data_v3.csv")


# # Temp dataframe for storing only required independent variables
temp = dataset[['segment_duration_sec', 'Reach', 'Time_hour', 'End_hour']]#]]
                #'start_sec', 'End_time', 'start_minutes', 'end_minutes']]#'AD_DURATION', 'PROMO_DURATION', 'segment_no']]#'Start_time_min']]#,'Reach']]
y = dataset['Break_min_filter'] # Dependent Variable


X_train = temp
y_train = y

import keras
y_train = keras.utils.to_categorical(y_train)#, num_classes=None, dtype='float32')



model = Sequential()
model.add(Dense(128, input_dim = 4, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.20))
model.add(Dense(2048, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(1024, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(9, activation='softmax'))

from keras.optimizers import SGD
opt = SGD(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
model.fit(X_train, y_train, epochs=64, batch_size=32,  verbose=1, validation_split=0.2)

###### Test File #########
test = pd.read_csv("data\\Test_data_v5_with_manual_values.csv")
temp = test[['segment_duration_sec', 'Reach', 'Time_hour', 'End_hour']] # 'start_sec', 'End_time',
             #'start_minutes', 'end_minutes']]#,'AD_DURATION',
             #'PROMO_DURATION', 'segment_no']]
X_test = temp
y_test = test['Break_min_filter']
y_test = y_test

############### Prediction ##############
y_pred = model.predict(X_test)

##### Accuracy #####
from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

# Making the Confusion Matrix
print(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted']))



label_array = y_train.reshape(-1, 1)
