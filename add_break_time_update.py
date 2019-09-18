# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:30:51 2019

@author: sdorle
"""

import pandas as pd
import numpy as np
from insert_row import Insert_row

# =============================================================================
#  Adding breaks in remaining positions
# =============================================================================
def add_break(df):
    # storing content_tpae_ids of movie
    content_tape_id = df.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(df.groupby('content_tape_id')))
       
    #final = pd.DataFrame()
    
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace = True)       
        
    final_hour_wise_group2 = dict(tuple(df.groupby('hour')))
        
    final_hours = list(final_hour_wise_group2.keys())
     
    
    #remove_break_dict = dict()
    add_break_dict = dict()
    
    count = 0
    
    #final_hours = [17]
    for hr in final_hours:
    
         b2 = final_hour_wise_group2.get(hr)
           
         tmp_hr = pd.DataFrame(b2)
        
         break_count = (tmp_hr.Break_Duration == 360).sum() # Counting the number of breaks in sepcific hour
            
         if break_count == 1:
             count += 1
             add_break_index = tmp_hr.Break_Duration[tmp_hr.Break_Duration == 0].index.tolist() # Indexes with no break in specific hour
             add_brk_content_tape_id = tmp_hr.loc[add_break_index[1], 'content_tape_id'] # selecting one index to add break out of all the indexes
             # adding index number and content tape id to dictionary         
             add_break_dict[add_break_index[1]] = add_brk_content_tape_id
            
    
    
    #remove_break_list = list(remove_break_dict.keys())
    add_break_list = list(add_break_dict.keys())
    
    # index numbers for adding breaks
    add_break_list.sort()
    for n in range(1, len(add_break_list)):
         add_break_list[n]  = add_break_list[n] + n
        
    # Adding breaks on specified indexes
    for ad in add_break_list:
        c_tape_id = df.loc[ad, 'content_tape_id']
        Insert_row(ad, df, [c_tape_id,0,0,0,0,0,360,0,0])
        df.sort_index(axis=0, inplace = True) 
        
    from time_update_function import time_update
    df3 = time_update(df)
    
    return df3