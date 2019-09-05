# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:40:22 2019

@author: sdorle
"""

import pandas as pd
import numpy as np
import random

# Importing Dataset 
dataset = pd.read_csv(r"C:\Users\sdorle\Desktop\saurabh\Break Optimization\\Data\\One_day_schedule\\30June2019_segment_wise.csv")#, usecols = [''])

# Selecting only imp features
#data = dataset[['segment_no', 'tape_dur_minute', 'Seg_start_hr', 'Seg_start_hr', 'Segment_start_min']]
data = dataset[['Seg_No', 'Segment_Start_Time_in_Min', 'Hour_num', 'Segment_dur_min', 'Segment_reach']]#, 'content_start_time_seconds']]#, 'Break_Dur_min', 'Total_Dur_Min']]

# Round/floor the value of Hour_num
data['Hour_num'] = data['Hour_num'].round(decimals=0)
# or
data['Hour_num'] = data['Hour_num'].apply(np.floor)


# New col for break duration
data['Break_Duration'] = pd.Series()
data['Break_Duration'] = 0

#data['Break_Duration'][1] = 1

# New col for Total duration 
#data['Total_Duration'] = data['Segment_dur_min'] + data['Break_Duration']

# Hour wise Dictionary of Dataframes
hour_wise_group = dict(tuple(data.groupby('Hour_num')))

hours = list(hour_wise_group.keys())


# =============================================================================
# Adding breaks for every Hour
# =============================================================================

hours = list(hour_wise_group.keys())

final = pd.DataFrame()
res = []
for i in hours:
    b = hour_wise_group.get(i)
    #final = pd.DataFrame()
    tmp = pd.DataFrame(b)
    tmp = tmp.reset_index()

    tmp.drop(['index'], axis=1, inplace = True)
    #res = []
    #res = random.sample(range(0, len(tmp)-1), 2)
    #res = random.sample(tmp.index.tolist(), 2)
    
    res = tmp.sort_values(['Segment_reach'], ascending=[1])

    res = res.index.tolist()
    
    # Assigning 7 min break at these 2 slots
    tmp.loc[res[0], 'Break_Duration'] = 7
    tmp.loc[res[1], 'Break_Duration'] = 7
    
    # Adding all the data to new dataframe
    final = final.append(tmp, ignore_index = True)#, sort = True)
     
    res.clear()
    del tmp


#==============================================================================
# Calculating Total Duration
final['Total_Duration'] = final['Segment_dur_min'] + final['Break_Duration']


# =============================================================================
# Start Time Updation  
# =============================================================================
# New Dataframe for storing startime values
duration = pd.DataFrame()

duration.at[0,'Start_Min'] = final.at[0,'Segment_Start_Time_in_Min']

for i in range(1, len(final)):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    duration.at[i,'Start_Min'] = duration.at[i-1,'Start_Min'] + final.at[i-1,'Total_Duration']
    
    
#duration.at[len(final)-1,'Start_Min'] = final.at[len(final)-1,'Segment_Start_Time_in_Min']
  

final['New_Start_Min'] = duration['Start_Min']
#final.to_csv("Data\\One_day_schedule\\results_reach_wise3.csv", index = False)

#final['Start_Min'] = duration['Start_Min']


final['Hour_num'] = (final['New_Start_Min'] / 60).apply(np.floor)
#final.to_csv("Data\\One_day_schedule\\results_reach_wise_with_hour_tmp_it1.csv", index = False)




# =============================================================================
# second interation
# =============================================================================

# New col for break duration
final['Break_Duration'] = pd.Series()
final['Break_Duration'] = 0
hour_wise_group2 = dict(tuple(final.groupby('Hour_num')))
hours2 = list(hour_wise_group2.keys())
hours2.remove(23.0)

final2 = pd.DataFrame()
res2 = []
for i in hours2:
    b = hour_wise_group2.get(i)
    #final = pd.DataFrame()
    tmp = pd.DataFrame(b)
    tmp = tmp.reset_index()

    tmp.drop(['index'], axis=1, inplace = True)
    #res = []
    #res = random.sample(range(0, len(tmp)-1), 2)
    #res = random.sample(tmp.index.tolist(), 2)
    
    res = tmp.sort_values(['Segment_reach'], ascending=[1])

    res = res.index.tolist()
    
    # Assigning 7 min break at these 2 slots
    tmp.loc[res[0], 'Break_Duration'] = 7
    tmp.loc[res[1], 'Break_Duration'] = 7
    
    # Adding all the data to new dataframe
    final2 = final2.append(tmp, ignore_index = True)#, sort = True)
     
    res2.clear()
    del tmp


#==========================================
# Calculating Total Duration
final2['Total_Duration'] = final2['Segment_dur_min'] + final2['Break_Duration']


# New Dataframe for storing startime values
duration = pd.DataFrame()

duration.at[0,'Start_Min'] = final2.at[0,'Segment_Start_Time_in_Min']

for i in range(1, len(final2)):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    duration.at[i,'Start_Min'] = duration.at[i-1,'Start_Min'] + final2.at[i-1,'Total_Duration']
    
    
#duration.at[len(final)-1,'Start_Min'] = final.at[len(final)-1,'Segment_Start_Time_in_Min']
  

final2['New_Start_Min'] = duration['Start_Min']
#final.to_csv("Data\\One_day_schedule\\results_reach_wise3.csv", index = False)

#final['Start_Min'] = duration['Start_Min']


final2['Hour_num'] = (final2['New_Start_Min'] / 60).apply(np.floor)

final2.to_csv("Data\\One_day_schedule\\results_reach_wise_with_hour_tmp_it2.csv", index = False)















'''
# Assigning 7 min break at these 2 slots
tmp.loc[res2[0], 'Break_Duration'] = 7
tmp.loc[res2[1], 'Break_Duration'] = 7

# Adding all the data to new dataframe
final = pd.DataFrame()
final = final.append(tmp, ignore_index = True)

tmp.drop()




res = b.sort_values(['Segment_reach'], ascending=[1])

for i in new:
    temp = new.get(i)
    print(temp[0])
    
    
    

for i in new:
    i.values()
    print(value)
    for j in i:
        print(j['HourNumber'])

temp = []

temp_reach = []
for index, rows in dataset.iterrows():
        if rows['Hr_Number'] == 7:
            temp_data.insert(rows)
            
            temp.append(rows)
            temp_reach.append(rows['Reach'])
            
print(temp_reach)
temp_reach.sort()

'''