# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:21:02 2019

@author: sdorle
"""


# # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Importing Dataset
dataset = pd.read_csv('train\\train2(sep_oct_2018).csv')


# # Temp dataframe for storing only required independent variables
temp = dataset[['DOW', 'Slot_Name', 'Start_time_min']]#,'Reach']]
y = dataset['Reach'] # Dependent Variable


# # Applying encoding on cetegorical vriables
X = pd.get_dummies(temp, columns=["DOW", "Slot_Name"])
X = X.values
y = y.values

'''
# Train Test splitting
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
'''
# =============================================================================
# # Fitting the Random Forest Regression Model to the dataset
# =============================================================================
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
regressor.fit(X, y)

'''
from sklearn.externals import joblib
# save the model to disk
filename = 'random_forest.sav'
joblib.dump(regressor, filename)'''

# =============================================================================
# Testing
# =============================================================================



dataset2 = pd.read_csv('test\\single_day.csv')

# # Temp dataframe for storing only required independent variables
test = dataset2[['DOW', 'Slot_Name', 'Start_time_min']]#,'Reach']]
y_test = dataset2['Reach'] # Dependent Variable


# # Applying encoding on cetegorical vriables
X_test = pd.get_dummies(test, columns=["DOW", "Slot_Name"])
X_test = X_test.values
y_test = y_test.values

'''
# load the model from disk
filename = 'random_forest.sav'
loaded_model = joblib.load(filename)'''

y_pred = regressor.predict(X_test) 

dataset2['Predict'] = y_pred

dataset2.to_csv("results2.csv")


import matplotlib.pyplot as plt
# Draw Plot
def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

plot_df(dataset2, x=dataset2.Start_time_min, y=dataset2.Predict, title='Title')   