# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:30:42 2019

@author: sdorle
"""


# # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Importing Dataset
dataset = pd.read_csv('Data\\train\\train_minute arranged.csv')


# # Temp dataframe for storing only required independent variables
temp = dataset[['DOW', 'Slot_Name', 'Minute_Number']]#'Start_time_min']]#,'Reach']]
y = dataset['Reach'] # Dependent Variable


# # Applying encoding on cetegorical vriables
X = pd.get_dummies(temp, columns=["Slot_Name"])

from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
X['DOW'] = labelencoder.fit_transform(X['DOW'])

X = X.values
y = y.values
  
# =============================================================================
# # Fitting the Random Forest Regression Model to the dataset
# =============================================================================
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
regressor.fit(X, y)


from sklearn.externals import joblib
# save the model to disk
filename = 'random_forest3.sav'
joblib.dump(regressor, filename)


# =============================================================================
# Testing
# =============================================================================


dataset2 = pd.read_csv('Data\\test\\single_day.csv')

# # Temp dataframe for storing only required independent variables
test = dataset2[['DOW', 'Slot_Name', 'Minute_Number']]#'Start_time_min']]#,'Reach']]
y_test = dataset2['Reach'] # Dependent Variable


# # Applying encoding on cetegorical vriables
X_test = pd.get_dummies(test, columns=["Slot_Name"])

X_test['DOW'] = labelencoder.fit_transform(X_test['DOW'])

X_test = X_test.values
y_test = y_test.values

'''
# load the model from disk
filename = 'random_forest.sav'
loaded_model = joblib.load(filename)'''

y_pred = regressor.predict(X_test) 

dataset2['Predict'] = y_pred

dataset2.to_csv("Results\\results3.csv")



# =============================================================================
# Performance Evaluation
# =============================================================================
from sklearn import metrics
from sklearn.metrics import r2_score

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('R Squared:', r2_score(y_test, y_pred))




import matplotlib.pyplot as plt
# Draw Plot
def plot_df(df, x, y, title="", xlabel='Minutes', ylabel='Avg_Reach', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

plot_df(dataset2, x=dataset2.Minute_Number, y=dataset2.Predict, title='Title')   

