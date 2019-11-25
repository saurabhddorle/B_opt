# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:36:57 2019

@author: sdorle
"""
'''
Procedure:  INSERT_FCT_TEST, parameter pass table

[schedule_detail_id] [int] NULL,
[content_tape_detail_id] [int] NULL,
[segment_duration_sec] [float] NULL,
[ad_duration_sec] [float] NULL,
[promo_duration_sec] [float] NULL,
[slot_id] [int] NULL,
[air_date] [datetime] NULL
'''

import pyodbc 
import pandas as pd
import numpy as np
import pytds
from pytds import login
import sqlalchemy as sa
from sqlalchemy import create_engine
import sqlalchemy_pytds


#cnxn = pyodbc.connect(dsn='MODB_9SEP', uid='sdorle', pwd='sdd@123')				
# Function for DB conntection
def connect():
    return pytds.connect(dsn='192.168.1.26', database = 'MODB@9SEP', user = 'sdorle', password = 'sdd@123', autocommit=True)#, auth=login.SspiAuth())

# Creating engine 
engine = sa.create_engine('mssql+pytds://MODB_9SEP', creator=connect)
conn = engine.raw_connection()


# =============================================================================
# 
# =============================================================================

results['air_date'] = pd.to_datetime(results['air_date']).dt.date

# Selecting single day from schedule
date_wise_group = dict(tuple(results.groupby('air_date')))

# storing content_tpae_ids of movie
air_dates = results.air_date.unique()

for d in range(0, len(air_dates)):#
    
    day = pd.DataFrame(date_wise_group.get(air_dates[d]))
    
    #day = day.reset_index()
    #day.drop(['index'], axis=1, inplace = True)
    
    # storing content_tpae_ids of movie
    schedule_detail_ids = day.schedule_detail_id.unique()
    
    # Hour wise Dictionary of Dataframes
    schedule_id_wise_group = dict(tuple(day.groupby('schedule_detail_id')))
    
    
    final_2 = pd.DataFrame()
    
    #schedule_detail_ids = [56631]
    #content_tape_id = [9140]

    for i in schedule_detail_ids:
        
        movie = pd.DataFrame(schedule_id_wise_group.get(i))

        # Storing all the rows of movie dataframe in 'arg'
        arg = [tuple(x) for y,x in movie.iterrows()]
        # creating Table Valued Parameter with all single movie table
        tvp = pytds.TableValuedParam(type_name='dbo.temp_sch_schedule_detail_fpc_test', rows= arg)
        engine.execute('EXEC INSERT_FCT_TEST %s', (tvp,)) # Executing the procedure by passing TVP
                
        
    