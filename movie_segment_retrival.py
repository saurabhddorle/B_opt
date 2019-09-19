# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:18:43 2019

@author: sdorle
"""

# =============================================================================
# 
# =============================================================================

# Connecting to SQL server
import pyodbc 
import pandas as pd
import numpy as np

#schedule = pd.read_csv(r"C:\Users\sdorle\Desktop\saurabh\Break Optimization\Data\One_day_schedule\\30June2019_V2.csv")
                       #,usecols = ['air_date', 'content_tape_id', 'content_name', 'Start_time', 'content_start_min'])
# Original File
schedule = pd.read_csv(r"C:\Users\sdorle\Desktop\saurabh\Break Optimization\Data\One_day_schedule\\one_day_schedule_modify.csv")

# Removing empty entries
schedule = schedule.loc[schedule['content_id']  != -1] 

# Connection establishment
'''
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=192.168.1.26;"
                        "Database=ZeeMODB@25June;"
                        "uid=sdorle;pwd=sdd@123") '''

# or
cnxn = pyodbc.connect(dsn='ZEE_25june', uid='sdorle', pwd='sdd@123')


# =============================================================================
# Adding segments of movies
# =============================================================================

# Mysql Query for retriving segments of movies based on content_tape_id
select_query = '''select rctd.content_tape_id,
                       rctd.content_tape_detail_name,
                       rctd.tape_duration_sec,
                       rctd.segment_no
                       from ref_content_tape_detail rctd
                       inner join  ref_content_tape rct on rctd.content_tape_id = rct.content_tape_id
                       inner join ref_content rc on rct.content_id = rc.content_id
                       where rct.content_tape_id = ''' 

# Storing all the content_tape_ids of movies
content_tape_id = list(schedule['content_tape_id']) 

# Creating new DataFrame to store retrived segments of all the movies
df3 = pd.DataFrame()
for i in content_tape_id:
    #var = select_query + str(i)
    temp = pd.read_sql_query(select_query + str(i), cnxn)
    # print(var)
    df3 = df3.append(temp)

#closing connection
cnxn.close()
#==============================================================================

# Reseting index of dataframe
df3 = df3.reset_index()
df3.drop(['index'], axis=1, inplace = True)


# Converting to Seconds format
schedule['Start_time'] = pd.to_timedelta(schedule['content_start_time'])
schedule['start_seconds'] = schedule['Start_time'].dt.total_seconds()

# Converting to datetime format
schedule['air_date'] = pd.to_datetime(schedule['air_date'])

# Seperating date and month
schedule['month'],schedule['day'] = schedule.air_date.dt.month, schedule.air_date.dt.day
 
# Retriving day of the week
schedule['dow'] = schedule['air_date'].dt.dayofweek


# =============================================================================
# # Get the index of First ouccurance of specifiied content_tape_id to assign the start time value
# =============================================================================
start_times = schedule['start_seconds'] # storing start time values

# Storing index locations of the movie start segment
locations = []
for j in content_tape_id:
    loc = df3.content_tape_id.ne(j).idxmin()
    locations.append(loc)
    
# adding start_sec column to dataframe
for j in range(0, len(schedule)):
    df3.at[locations[j], 'Start_seconds'] = schedule.at[j, 'start_seconds']
    # or
    #df3.at[locations[j], 'Start_sec'] = start_times[j]
    
# Adding day, month and DOW to segment file
df3['month'] = schedule['month']
df3['day'] = schedule['day']
df3['dow'] = schedule['dow']

df3['month'] = df3['month'].ffill(axis = 0)
df3['day'] = df3['day'].ffill(axis = 0)
df3['dow'] = df3['dow'].ffill(axis = 0)
#==============================================================================



# Groupby content_tape_id
grp = dict(tuple(df3.groupby('content_tape_id')))

# New Dataframe for storing all start time in seconds for all sengments
final_ = pd.DataFrame()

# Calculatinf start time of segments based on movie start time
for i in content_tape_id:
    #final = pd.DataFrame()
    tmp = grp.get(i)
    tmp = tmp.reset_index()
    tmp.drop(['index'], axis=1, inplace = True)
    
    for i in range(1, len(tmp)):
        tmp.at[i,'Start_seconds'] = tmp.at[i-1,'Start_seconds'] + tmp.at[i-1,'tape_duration_sec']
        
    final_ = final_.append(tmp, ignore_index = True)#, sort = True)        
    del tmp
    


# Converting to hour format
final_['hour'] = (final_['Start_seconds'] / 3600).apply(np.floor)
    
#final_.to_csv("temp_one_day_with_segments.csv", index = False)


# or
cnxn = pyodbc.connect(dsn='ZEE_25june', uid='sdorle', pwd='sdd@123')

cnxn.close()

