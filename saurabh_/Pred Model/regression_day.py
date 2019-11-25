# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 11:45:43 2019

@author: sdorle
"""


# =============================================================================
# # Importing Libraries
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# # Importing Dataset
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
# # Fitting the Random Forest Regression Model to the dataset
# =============================================================================
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test) # predicting test set

from math import sqrt
from sklearn.metrics import mean_squared_error
rms = sqrt(mean_squared_error(y_test, y_pred)) # Calculating root mear square error
print(rms)

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)  


'''
errors = abs(y_pred - y_test)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)
print('mape:', round(np.mean(mape), 2), '%.')
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')'''

# =============================================================================
# Fitting Linear Regressor 
# =============================================================================
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test) # predicting test set

from math import sqrt
from sklearn.metrics import mean_squared_error
rms = sqrt(mean_squared_error(y_test, y_pred)) # Calculating root mear square error
print(rms)



# =============================================================================
# Fitting XGBoost to the Training set
# =============================================================================
from xgboost import XGBRegressor
regressor = XGBRegressor()
regressor.fit(X_train, y_train) 

y_pred = regressor.predict(X_test) # predicting test set

from math import sqrt
from sklearn.metrics import mean_squared_error
rms = sqrt(mean_squared_error(y_test, y_pred)) # Calculating root mear square error
print(rms)




