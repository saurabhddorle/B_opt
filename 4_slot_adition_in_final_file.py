# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:49:42 2019

@author: sdorle
"""

import pyodbc 
import pandas as pd
import numpy as np

##Database Connection
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=192.168.1.26;"
                        "Database=ZeeMODB@25June;"
                        "uid=sdorle;pwd=sdd@123") 

#qyery to fetch slot name
sql_select_Query = ''' select top 7 slot_desc,slot_start_time from ref_slot'''

df4 = pd.read_sql_query(sql_select_Query, cnxn)   
cnxn.close()


df4['slot_start_hour'] = pd.to_datetime(df4['slot_start_time'], format='%H:%M:%S').dt.hour

df5 = pd.DataFrame()
df5  = final3.join(df4.set_index('slot_start_hour'), on=['hour'])
df5 = df5.drop(['slot_start_time'], axis=1)

df5['slot_desc'] = df5['slot_desc'].ffill(axis = 0)
df5 = df5.fillna('Subah 1')
#df5.to_csv("17-09-2019_break_add_row_wise_all_movies_final_with_time_12min_break_slot.csv",index = False)
