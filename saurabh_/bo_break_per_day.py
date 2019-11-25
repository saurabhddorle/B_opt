# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 11:57:40 2019

@author: Saurabh
"""


#import time
#start_time = time.clock()

import pandas as pd
import numpy as np
import sys
from fun1 import get_break_dur, low_reach, round_off
from fun_time_updation import *
from bo_break_per_movie import break_per_movie

#abc = single_day_break(predicted)

def single_day_break(day_1):
    movie_check = []
    #day_1 = predicted 
    #dataset = pd.read_csv("data\\One_day_schedule_with_reach.csv")#1June.csv")#
    data_2 = day_1[['air_date', 'SCHEDULE_DETAIL_ID', 'CONTENT_TAPE_DETAIL_ID', 'content_tape_id', 
                    'segment_no', 'tape_duration_sec', 'hour', 'Reach', 'Start_seconds', 'end_sec', 
                    'slot_id', 'AD_DURATION', 'PROMO_DURATION']]
    
    
    # storing content_tpae_ids of movie
    content_tape_id = data_2.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(data_2.groupby('content_tape_id')))
    
    
    final_2 = pd.DataFrame()
    
    #content_tape_id = [12521]
    #content_tape_id = [9140]
    movie_count = 0
        
    for i in content_tape_id:
        
        movie_count += 1
        
        movie = pd.DataFrame(tape_id_wise_group.get(i))
        movie = movie.reset_index()                     # Resetting the index
        movie.drop(['index'], axis=1, inplace = True)   
        
        movie['break_min'] = pd.Series()
        movie['break_min'] = 0
          
        
        ''' Get Break duration for respective hours  '''
        hours_dict = get_break_dur(movie)
        
        
        movie['Time_hour'] = (movie['Start_seconds'] / 3600).apply(np.floor)
        movie['Time_hour'].iloc[-1] = (movie['end_sec'].iloc[-1] / 3600).astype(int)# setting last hour value
        
        
        
       ############ Set the breaks for respected hours and then update the time ##################
    
        unique_hours = movie.Time_hour.unique()
    
        locations = []
        for k in unique_hours:
            loc = movie.Time_hour.ne(k).idxmin()
            locations.append(loc)
        
        for l, m in  zip(unique_hours, locations):
            movie['break_min'].iloc[m] = hours_dict.get(l)
            
           
        # Time update
        movie['Total_Duration'] = movie['tape_duration_sec'] + movie['break_min'] 
        movie.at[0,'start_sec'] = movie.at[0,'Start_seconds']  
        # Segment time updation
        for k in range(1, len(movie)):
            #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
            movie.at[k,'start_sec'] = movie.at[k-1,'start_sec'] + movie.at[k-1,'Total_Duration']
                
        movie['Time_hour'] = (movie['start_sec'] / 3600).apply(np.floor)
        
        movie.drop(columns = ['hour', 'Start_seconds', 'end_sec', 'Time_format', 'Time_minutes'], inplace = True)
        
        
        movie['End_time'] = 0
        movie['End_hour'] = 0
        movie = time_update.start_time_update(movie)
        movie = time_update.end_time_update(movie)      
        
        movie['break_min'] = 0
        
        # Total breaks duration
        total_break_per_hr_2 = (movie['AD_DURATION'].iat[0] + movie['PROMO_DURATION'].iat[0]) / 60
        
        try:
            movie_with_break = break_per_movie(movie, hours_dict, total_break_per_hr_2)
            movie_with_updated_breaks = round_off(movie_with_break)
            final_2 = final_2.append(movie_with_updated_breaks)
            del movie, movie_with_break

        except:
            print("\nError for placing breaks in Movie content_tape_id:", movie['content_tape_id'].iloc[0])
            movie_check.append(movie['content_tape_id'].iloc[0])
            #print("\n : ",sys.exc_info()[0])
        
        
        
        #final_2 = final_2.append(movie_with_break)
        
        #del movie, movie_with_break
        
        
    #final['start_time_in_time'] = pd.to_datetime(final['start_sec'], unit = 's').dt.time
    #final['End_Time_in_time'] = pd.to_datetime(final['End_time'], unit = 's').dt.time 
    
    final_2['start_time_in_time'] = final_2['start_sec'].astype('datetime64[s]').dt.time
    final_2['end_time_in_time'] = final_2['End_time'].astype('datetime64[s]').dt.time
    
    
    return final_2, movie_check    
        
    
#print(time.clock() - start_time, "seconds")   
    
    

    