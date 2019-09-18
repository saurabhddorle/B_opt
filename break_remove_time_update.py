# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:48:28 2019

@author: sdorle
"""

import pandas as pd
import numpy as np

# =============================================================================
# Removing extra breaks and adding reamining breaks
# =============================================================================

def remove_break(df):
    
    # storing content_tpae_ids of movie
    content_tape_id = df.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(df.groupby('content_tape_id')))
    
    
    #final = pd.DataFrame()
    
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace = True)       
        
    final_hour_wise_group2 = dict(tuple(df.groupby('hour')))
        
    final_hours = list(final_hour_wise_group2.keys())
     
    
    remove_break_dict = dict()
    #add_break_dict = dict()
    
    count = 0
    
    #final_hours = [17]
    for hr in final_hours:
    
         b2 = final_hour_wise_group2.get(hr)
           
         tmp_hr = pd.DataFrame(b2)
        
         break_count = (tmp_hr.Break_Duration == 360).sum() # Counting the number of breaks in sepcific hour
         
         if break_count > 2:
             count += 1
             all_break_index = tmp_hr.Break_Duration[tmp_hr.Break_Duration == 360].index.tolist() # Indexes having break scheduled
             remove_break_index = all_break_index[1::2]        
             for br in remove_break_index:
                 brk_content_tape_id = tmp_hr.loc[br, 'content_tape_id'] # out of all break indexes, selecting one index to remove
                 # adding index number and content tape id to dictionary         
                 remove_break_dict[br] = brk_content_tape_id
                 
           
    remove_break_list = list(remove_break_dict.keys())
    #add_break_list = list(add_break_dict.keys())
    
    remove_break_list.sort()
    for rm in remove_break_list:
        #final.at[rm, 'Break_Duration'] = 0
        df = df.drop(rm)
    
    from time_update_function import time_update
    df2 = time_update(df)
    
    return df2