# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:10:28 2019

@author: sdorle
"""

import pandas as pd
import numpy as np
# =============================================================================
# Updating time of all movies after filtering added breaks
# =============================================================================    

def time_update(df):
    
    # storing content_tpae_ids of movie
    content_tape_id = df.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(df.groupby('content_tape_id')))
    
    content_tape_id = df.content_tape_id.unique()
    
    
    final_filtered = pd.DataFrame()
    
    for i in content_tape_id:
        
        # Selcet one movie
        movie = pd.DataFrame(tape_id_wise_group.get(i))
    
        movie = movie.reset_index()
        movie.drop(['index'], axis=1, inplace = True)   
    
        # Groupby hour
        hour_wise_group = dict(tuple(movie.groupby('hour')))
        
        # Stroring hours 
        hours = list(hour_wise_group.keys())
        
        
        # calculating total duration based on added break values
        movie['Total_Duration'] = movie['tape_duration_sec'] + movie['Break_Duration']
    
        # Setting first starging value as it is
        if movie.at[0,'Start_seconds'] == 0:
            movie.at[0,'start_sec'] = movie.at[1,'Start_seconds']
        else:
            movie.at[0,'start_sec'] = movie.at[0,'Start_seconds']
        
        # Segment time updation
        for k in range(1, len(movie)):
            #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
            movie.at[k,'start_sec'] = movie.at[k-1,'start_sec'] + movie.at[k-1,'Total_Duration']
    
        # Calculating hours based on new time
        movie['hour'] = (movie['start_sec'] / 3600).apply(np.floor)
        # Groupby based on new calculated hours
        hour_wise_group = dict(tuple(movie.groupby('hour')))
        final_filtered = final_filtered.append(movie)
    
    return final_filtered
        
    #final_filtered.to_csv("16-09-2019_Final_filtered_row_add.csv", index = False)