# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:47:24 2019

@author: sdorle
"""


# # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Importing Dataset
dataset = pd.read_csv("data\\Train_data_v3.csv")


# # Temp dataframe for storing only required independent variables
temp = dataset[['segment_duration_sec', 'Reach', 'Time_hour', 'End_hour']]#]]
                #'start_sec', 'End_time', 'start_minutes', 'end_minutes']]#'AD_DURATION', 'PROMO_DURATION', 'segment_no']]#'Start_time_min']]#,'Reach']]
y = dataset['Break_min_filter'] # Dependent Variable
#temp = temp.head(100)
#y = y.head(100)

X_train = temp.values
y_train = y.values
  

#from sklearn.model_selection import train_test_split

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

#################### Model Training #######################
from sklearn.ensemble import RandomForestClassifier
# Fitting Random Forest Classification to the Training set
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42)
classifier.fit(X_train, y_train)

###### Test File #########
test = pd.read_csv("data\\Test_data_v5_with_manual_values.csv")
temp = test[['segment_duration_sec', 'Reach', 'Time_hour', 'End_hour']] # 'start_sec', 'End_time',
             #'start_minutes', 'end_minutes']]#,'AD_DURATION',
             #'PROMO_DURATION', 'segment_no']]
X_test = temp.values
y_test = test['Break_min_filter']
y_test = y_test.values

#### Prediction #####
y_pred = classifier.predict(X_test)

##### Accuracy #####
from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

# Making the Confusion Matrix
print(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted']))

# =============================================================================
# SVM
# =============================================================================
# training a linear SVM classifier 
from sklearn.svm import SVC 
svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train) 
svm_predictions = svm_model_linear.predict(X_test)
  
# model accuracy for X_test   
accuracy = svm_model_linear.score(X_test, y_test) 
  
# creating a confusion matrix 
cm = confusion_matrix(y_test, svm_predictions) 

from sklearn import svm
SVM = svm.SVC(decision_function_shape="ovo").fit(X_train, y_train)
SVM.predict(X_test)
round(SVM.score(X_test, y_test), 4)


# =============================================================================
# Performance Evaluation
# =============================================================================

from sklearn.metrics import r2_score
print('R Squared:', r2_score(y_test, y_pred))
