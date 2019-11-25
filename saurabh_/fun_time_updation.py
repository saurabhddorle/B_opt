# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:22:27 2019

@author: sdorle
"""

import pandas as pd
import numpy as np

class time_update:
    
    
    def start_time_update(df1):
        
        # calculating total duration based on added break values
        df1['Total_Duration'] = df1['tape_duration_sec'] + df1['break_min'] 
        
         # Setting first starging value as it is
        if df1['start_sec'].iloc[0] == 0:
            df1['start_sec'].iloc[0] = df1['start_sec'].iloc[1]
        else:
            df1['start_sec'].iloc[0] = df1['start_sec'].iloc[0]
       
        # movie.at[0, 'start_sec'] = movie.at[0, 'Start_seconds']
        # Segment time updation
        for k in range(1, len(df1)):
            #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
            df1['start_sec'].iloc[k] = df1['start_sec'].iloc[k-1] + df1['Total_Duration'].iloc[k-1]
    
        df1['Time_hour'] = (df1['start_sec'] / 3600).apply(np.floor)
        
        
        return df1
    
    
    
    
    def end_time_update(df2):
        
        # Setting first starging value as it is
        df2['End_time'].iloc[0] = df2['start_sec'].iloc[0]
     
        # End time updation
        for l in range(0, len(df2)):
            #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
            df2['End_time'].iloc[l] = df2['start_sec'].iloc[l] + df2['Total_Duration'].iloc[l]
            
        df2['End_hour'] = (df2['End_time']/ 3600).apply(np.floor)
        
        return df2
        
        
        
        
        