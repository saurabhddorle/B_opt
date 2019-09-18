# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:39:20 2019

@author: sdorle
"""

import pandas as pd
import numpy as np
# =============================================================================
#  Get the count of hours with extra breaks
# =============================================================================
def get_extra_break_count(df):
    
    # storing content_tpae_ids of movie
    content_tape_id = df.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(df.groupby('content_tape_id')))
       
    
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace = True)       
        
    final_hour_wise_group2 = dict(tuple(df.groupby('hour')))
        
    final_hours = list(final_hour_wise_group2.keys())
     
    count = 0
    

    for hr in final_hours:
    
         b2 = final_hour_wise_group2.get(hr)
           
         tmp_hr = pd.DataFrame(b2)
        
         break_count = (tmp_hr.Break_Duration == 360).sum() # Counting the number of breaks in sepcific hour
         
         if break_count > 2:
             count += 1
    
    return count


def get_add_break_count(df):
     # storing content_tpae_ids of movie
    content_tape_id = df.content_tape_id.unique()
    
    # Hour wise Dictionary of Dataframes
    tape_id_wise_group = dict(tuple(df.groupby('content_tape_id')))
       
    
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace = True)       
        
    final_hour_wise_group2 = dict(tuple(df.groupby('hour')))
        
    final_hours = list(final_hour_wise_group2.keys())
    
    count2 = 0
    
    for hr in final_hours:
    
         b2 = final_hour_wise_group2.get(hr)
           
         tmp_hr = pd.DataFrame(b2)
        
         break_count = (tmp_hr.Break_Duration == 360).sum() # Counting the number of breaks in sepcific hour
            
         if break_count == 1:
             count2 += 1
    
    return count2
            
    
    