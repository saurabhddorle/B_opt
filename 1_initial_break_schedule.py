# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:40:27 2019

@author: sdorle
"""

from insert_row import Insert_row

#Insert_row(row_number, df, row_value)

# =============================================================================
#  Adding Initial breaks and updating time based on added breaks
# =============================================================================
import pandas as pd
import numpy as np
import random
from fun_res2 import low_reach

# Importing Dataset 
dataset = pd.read_csv("data\\One_day_schedule_with_reach.csv")#, usecols = [''])

# Selecting only imp features
data = dataset[['content_tape_id', 'segment_no', 'tape_duration_sec', 'hour', 'Reach', 'Start_seconds']]

# New col for break duration
data['Break_Duration'] = pd.Series()
data.loc[:,'Break_Duration'] = 0

data['Total_Duration'] = pd.Series()
data.loc[:,'Total_Duration'] = 0

data['start_sec'] = pd.Series()
data.loc[:,'start_sec'] = 0


# storing content_tpae_ids of movie
content_tape_id = data.content_tape_id.unique()

# Hour wise Dictionary of Dataframes
tape_id_wise_group = dict(tuple(data.groupby('content_tape_id')))


final = pd.DataFrame()

#content_tape_id = [3999]

for i in content_tape_id:
    
    # Selcet one movie
    #b = tape_id_wise_group.get(i)
    
    # Selecting single movie from the data
    movie = pd.DataFrame(tape_id_wise_group.get(i))
    movie = movie.reset_index()                     # Resetting the index
    movie.drop(['index'], axis=1, inplace = True)   

    # Groupby hour on single movie
    hour_wise_group = dict(tuple(movie.groupby('hour')))
    
    # Stroring hour numbers of single movie
    hours = list(hour_wise_group.keys())
    
    #hours = [23]
    # iterating through all the hours to add the breaks
    for j in hours:
        
        #b2 = hour_wise_group.get(j)
        # Storing single hour in tmp dataframe
        tmp = pd.DataFrame(hour_wise_group.get(j))
    
        # Checking size of tmp, if only single record is available then add single break only
        if len(tmp) < 2:
            res = tmp.index.tolist()
            Insert_row(res[0], movie, [i,0,0,0,0,0,360,0,0])
            movie.sort_index(axis=0, inplace = True) 
            
        else:
            # Storing index numbers with low reach in res variable
            res = low_reach(tmp)
            del res[2:]
            res.sort()# keeping only first two index numbers to add two breaks
            
            
            Insert_row(res[0], movie, [i,0,0,0,0,0,360,0,0])
            movie.sort_index(axis=0, inplace = True) 
            Insert_row(res[1] + 1, movie, [i,0,0,0,0,0,360,0,0])
            movie.sort_index(axis=0, inplace = True) 

                
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
        
        
    # Adding updated movie breaks to dataframe
    final = final.append(movie)
    #tape_id_wise_group = dict(tuple(data.groupby('content_tape_id')))

#final.to_csv("16-09-2019_final_row_add.csv", index = False)

