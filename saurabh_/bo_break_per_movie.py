# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:47:29 2019

@author: Saurabh
"""

from fun1 import low_reach, dead_band_break_rem
from fun_time_updation import *

def break_per_movie(movie_1, hours_dict, total_break_per_hour):
    
    hour_count = 0
    
    # Stroring hour numbers of single movie
    hours = list(hours_dict.keys())
    hours.sort()
    
    hour_wise_group = dict(tuple(movie_1.groupby('End_hour')))
    
    #hours = [17]
    ################# iterating through all the hours to add the breaks ######################
    for j in hours:
        
        hour_count += 1
        
        # stroing single hour in temp dataframe
        tmp = pd.DataFrame(hour_wise_group.get(j))
        
        if len(tmp) != 0:
            
            # Calculating break duration
            if len(tmp) >= 2:            
                break_dur2 =  hours_dict.get(j)
                if break_dur2 > 240:
                    break_dur = break_dur2 / 2
                    break_count = 2
                else:
                    break_dur = break_dur2
                    break_count = 1
                    
            else:
                break_dur2 =  hours_dict.get(j)
                break_dur = break_dur2
                if break_dur == total_break_per_hour:
                    hours_dict.update({j : 0})
                    break_count = 0
                else:
                    break_count = 1
                    break_count = 1
                
            
            ####################################### adding break #################
            if break_count == 1:
                res = low_reach(tmp)
                # add break
                movie_1['break_min'].iloc[res[0]] = break_dur
                # updating time
                movie_1 = time_update.start_time_update(movie_1)
                movie_1 = time_update.end_time_update(movie_1) 
            
            if break_count == 2:         
                 res = low_reach(tmp)
                 # To manage the slipping break at first hour of movie
                 if hour_count == 2:
                     res = [x for x in res if movie_1['break_min'].iloc[x] == 0]
                 
                 del res[2:]
                 res.sort()
                 
                 # add first break
                 movie_1['break_min'].iloc[res[0]] = break_dur
                 # update time
                 movie_1 = time_update.start_time_update(movie_1)
                 movie_1 = time_update.end_time_update(movie_1) 
                 #if movie['End_hour'].iloc[res[0]] == movie['Time_hour'].iloc[res[0]] + 1:
                 #    movie['break_min'].iloc[res[0]] = 0
                  #   movie['break_min'].iloc[res[0]-1] = break_dur
                     
                 
                 
                 # Make hour wise group on updated time
                 hour_wise_group_2 = dict(tuple(movie_1.groupby('End_hour')))
                 # storing single hour in temp dataframe
                 tmp_2 = pd.DataFrame(hour_wise_group_2.get(j))
                 # getting low reach values         
                 res_2 = low_reach(tmp_2)
                 # removing index with first break
                 res_2 = [x for x in res_2 if movie_1['break_min'].iloc[x] == 0] # res_2.remove(res[0])
                 # adding second break
                 movie_1['break_min'].iloc[res_2[0]] = break_dur
                 
                 # updating time
                 movie_1 = time_update.start_time_update(movie_1)
                 movie_1 = time_update.end_time_update(movie_1) 
                 
                 #### for slipping break in next hour #####
                 res_3 = [res[0], res_2[0]]
                 res_3.sort()
             
                 if movie_1['End_hour'].iloc[res_3[1]] == movie_1['Time_hour'].iloc[res_3[1]] + 1:
                     movie_1['break_min'].iloc[res_3[1]] = 0
                     if movie_1['break_min'].iloc[res_3[1]-1] == 0:
                         movie_1['break_min'].iloc[res_3[1]-1] = break_dur
                     else:
                         movie_1['break_min'].iloc[res_3[1]-2] = break_dur
                     
        
            hour_wise_group = dict(tuple(movie_1.groupby('End_hour')))
            del tmp
            
        
    ######################## manage remaining time   ####################################### 
    hours_2 = list(movie_1.End_hour.unique().astype(int)) # Ending hours
    hours_3 = list(movie_1.Time_hour.unique().astype(int)) # Starting hours
    hours_4 = list(set(hours_2 + hours_3)) # union of start and end hours
    
    # list to store hour values
    breaks = []
    for br in hours_4:
        breaks.append(hours_dict.get(br))
        
    # total breaks need to be placed   
    total_breaks = sum(breaks)
    # acutal breaks placed
    actual_breaks = sum(movie_1['break_min'])
    # ramaining breaks
    difference = total_breaks - actual_breaks
        
    if difference > 30:
        #print('\n Content_tape_id: ', movie_1['content_tape_id'].iloc[0])
        
        # available indexes to place breaks
        available_index = movie_1.index[movie_1['break_min'] == 0].tolist()
        
        # placing break in available index
        #movie_1['break_min'].iloc[available_index[-1]] = difference
        
        # placing break in available index
        if movie_1['break_min'].iloc[0] != 0:
            movie_1['break_min'].iloc[available_index[0]] =  movie_1['break_min'].iloc[0]
            movie_1['break_min'].iloc[0] = difference
        
        else:
            movie_1['break_min'].iloc[available_index[0]] = difference
             
        # upatign time after palcing break
        movie_1 = time_update.start_time_update(movie_1)
        movie_1 = time_update.end_time_update(movie_1) 
    
    
    # Removing breaks at the end segment
    if movie_1['break_min'].iloc[-1] != 0:
        # available indexes to place breaks
        available_index = movie_1.index[movie_1['break_min'] == 0].tolist()
        movie_1['break_min'].iloc[available_index[-1]] =  movie_1['break_min'].iloc[-1]
        
        movie_1['break_min'].iloc[-1] = 0
        
        # upatign time after palcing break
        movie_1 = time_update.start_time_update(movie_1)
        movie_1 = time_update.end_time_update(movie_1) 
        
    
    movie_1 = dead_band_break_rem(movie_1)
    
    return movie_1
      
    