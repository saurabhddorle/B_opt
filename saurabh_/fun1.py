# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:11:48 2019

@author: sdorle
"""

import pandas as pd
import numpy as np
from fun_time_updation import time_update
from sklearn.externals import joblib
from fun_time_updation import *

def get_break_dur(df):

    #df = movie
    
    df.at[0,'end_sec'] = df.at[0, 'Start_seconds']
    df['Time_format'] = pd.to_datetime(df['end_sec'], unit = 's').dt.time
    
    # getting hours
    df['Time_hour'] = pd.to_datetime(df['end_sec'], unit = 's').dt.hour
    
        
    hours = []
    hours.append(int(df['Time_hour'].iloc[0]))
    hours.append(int(df['Time_hour'].iloc[-1]))
    
    # To manage the hours after 12 AM      
    if hours[0] > 19 and hours[1] < 10:
        hours[1] += 24
        df['Time_hour'].iloc[-1] = hours[1]
    
    # getting all hours in the movie
    hours2 = []
    for i in range(hours[0],hours[1]+1):
        hours2.append(i)
       
    # selecting hours with 14 min breaks i.e. complete hours    
    hours2 = [x for x in hours2 if x not in hours]
   
    
    
    total_break_per_hr = (df['AD_DURATION'].iat[0] + df['PROMO_DURATION'].iat[0]) / 60
    # getting fractions of break
    df['Time_minutes'] = pd.to_datetime(df['end_sec'], unit = 's').dt.minute
    df['break_min'].iloc[0] = ((60 - df['Time_minutes'].iloc[0])/60) * total_break_per_hr
    df['break_min'].iloc[-1] = (df['Time_minutes'].iloc[-1]/60) * total_break_per_hr
    
   
    first = (df['break_min'].iloc[0]) * 60
    last = (df['break_min'].iloc[-1]) * 60
    
    if first == 0 :
      first = total_break_per_hr * 60
    if last == 0:
      last = total_break_per_hr * 60
        
    hours_dict = dict()
    hours_dict[hours[0]] = first#.astype(int)
    hours_dict[hours[1]] = last#.astype(int)
   
    for h in range(0, len(hours2)):
        hours_dict[hours2[h]] = total_break_per_hr * 60
    
    last_hr = df['Time_format'].iloc[-1]
    if last_hr.minute == 0:
         hours_dict[hours[1]] = 0
        
        
    
    return hours_dict


# =============================================================================
# Function for sorting the single hour dataframe based on reach
# =============================================================================

def low_reach(df):
    # Sorting based on reach values  
    reach_result = df.sort_values(['Reach'], ascending=[1])
    reach_result = reach_result.index.tolist()

    return reach_result


# =============================================================================
# Function for reach Prediction 
# =============================================================================

def reach_prediction(df):
    
    #from sklearn.externals import joblib
      
    X = df[['Month','Dow_id','hour','Start_seconds','tape_duration_sec']]
   
    # load the model from disk
    filename = 'trained_model\\trained.sav'
    model = joblib.load(filename)
    pred_model = model.predict(X) 
    
    ##Add reach to dataframe
    df['Reach'] = pred_model
    
    return df

# =============================================================================
# Round Off break Duration
# =============================================================================

def round_off(df):
    
    df['break_in_min'] =  df['break_min'].astype('datetime64[s]')
    df['break_in_min'] =  pd.to_datetime(df['break_in_min'])
    
    # Round off by second
    round_off_value = df['break_in_min'].dt.round('10S').dt.time  
    # Round off by minute
    #new = results['break_in_min'].dt.round('1min').dt.time  
    df['break'] = round_off_value
    
    ##convert time to seconds format
    df['break_2'] = pd.to_timedelta(df['break'].astype(str))        
    df['break_3'] = df['break_2'].dt.total_seconds()
    
    df['break_min'] = df['break_3']
    
    df.drop(columns=['break_in_min', 'break', 'break_2', 'break_3'], inplace = True)
    
    df = time_update.start_time_update(df)
    df = time_update.end_time_update(df) 
    
    return df

# =============================================================================
# Remove breaks after 1 am
# =============================================================================

def dead_band_break_rem(df):
    
    for i in range(0, len(df)):
       if df['End_hour'].iloc[i] in range(1,3) or df['End_hour'].iloc[i] >= 25:
           df['break_min'].iloc[i] = 0
        
        
        #if df['End_time'].iloc[i] >= 90000:
        #   df['break_min'].iloc[i] = 0
            
    df = time_update.start_time_update(df)
    df = time_update.end_time_update(df)  
    
    return df