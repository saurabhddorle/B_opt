# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 12:11:51 2019

@author: sdorle
"""

# =============================================================================
#  Importing the libraries
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
#  Importing the dataset
# =============================================================================
dataset = pd.read_csv('Week_40_(1-6_Oct).csv')

# =============================================================================
# # Temp dataframe for storing only required independent variables
# =============================================================================
temp = dataset[['DOW', 'Slot_Name', 'Start_time_min']]#,'Reach']]
y = dataset['Reach'] # Dependent Variable

# =============================================================================
# # Applying encoding on cetegorical vriables
# =============================================================================
X = pd.get_dummies(temp, columns=["DOW", "Slot_Name"])
X = X.iloc[:,:].values
y = y.values

# =============================================================================
# Train Test splitting
# =============================================================================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
# =============================================================================
# Model Building
# =============================================================================
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(30, activation='relu', input_dim = 15, kernel_initializer='normal'))
model.add(Dense(50, activation='relu'))
#model.add(Dense(1, kernel_initializer='normal'))
model.add(Dense(1, kernel_initializer='normal'))#activation='linear'))
model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mae','mse']) #mse reduced with sgd or rsmsprop

model.fit(X_train, y_train, epochs=32, batch_size=8)

y_pred = model.predict(X_test) # Prediction


#Model Evaluation
from math import sqrt
from sklearn.metrics import mean_squared_error
rms = sqrt(mean_squared_error(y_test, y_pred)) # Calculating root mear square error
print(rms)