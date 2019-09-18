# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 16:29:39 2019

@author: sdorle
"""

# Importing libraries
import pandas as pd
from insert_row import Insert_row

# storing data in new dataframe
final3 = final2

# Resetting the index
final3 = final3.reset_index()
final3.drop(['index'], axis=1, inplace = True)       
        
# Adding new column for end time
final3['End_time'] = pd.Series()
final3['End_time'] = 0


# Setting first starging value as it is
final3.at[0,'End_time'] = final3.at[0,'start_sec']


# End time updation
for k in range(0, len(final3)):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    final3.at[k,'End_time'] = final3.at[k,'start_sec'] + final3.at[k,'Total_Duration']
    

# New column for calculating the time remaining    
final3['Difference'] = pd.Series()
final3['Difference'] = 0


# Differene in time updation
for m in range(0, len(final3)-1):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    final3.at[m,'Difference'] = final3.at[ m + 1,'start_sec'] - final3.at[m,'End_time']
    

# Getting the index and values where time is reamaining
result = final3['Difference'].nonzero()
values = final3['Difference'].iloc[result] 

# Storing index numbers
index_num = values.index.values.tolist() 
# storing values of time to add break
values2= values.tolist()

# Updating index values (index values will change after adding rows, so here updating in advance)
index_num = [x+1 for x in index_num]
for n in range(1, len(index_num)):
    index_num[n]  = index_num[n] + n
        
# Adding remaining time as break in the specified index positions
for o, p in zip(index_num, values2):
    # Adding breaks on specified indexes 
    c_tape_id = final3.loc[o, 'content_tape_id']
    Insert_row(o, final3, [0,0,0,0,0,0,p,0,0,0,0,0])
    final3.sort_index(axis=0, inplace = True) 
    
    
    

# Dropping columns if not required
final3.drop(columns = ['start_time', 'End_time', 'Difference'], axis = 0, inplace = True)

# Calculating total duration after adding remaining breaks
final3['Total_Duration'] =  final3['tape_duration_sec'] + final3['Break_Duration']

# Start time updation
for k in range(1, len(final3)):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    final3.at[k,'start_sec'] = final3.at[k-1,'start_sec'] + final3.at[k-1,'Total_Duration']
    
    
    
# =============================================================================
#     End time updation
# =============================================================================
final3['Start_time'] = pd.to_datetime(final3['start_sec'], unit='s').dt.time

final3['End_time'] = pd.Series()
final3['End_time'] = 0

# Setting first starging value as it is
final3.at[0,'End_time'] = final3.at[0,'start_sec']

# Segment time updation
for k in range(0, len(final3)):
    #duration.at[i,'Start_Min'] = final.at[i,'Segment_Start_Time_in_Min']
    final3.at[k,'End_time'] = final3.at[k,'start_sec'] + final3.at[k,'Total_Duration']
    
    
final3['hour'] = (final3['start_sec'] / 3600).apply(np.floor)   
    
final3['End_time_'] = pd.to_datetime(final3['End_time'], unit='s').dt.time

# Saving csv file
#final3.to_csv("17-09-2019_Fina_breaks_added_with_differnce_covered2.csv", index = False)