# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:13:37 2019

@author: sdorle
"""

from fun_time_updation import *

for i in range(0, len(results)):
    if results['End_time'].iloc[i] >= 90000:
        results['break_min'].iloc[i] = 0
        

movie = results
movie = time_update.start_time_update(movie)
movie = time_update.end_time_update(movie)  

 
movie['start_time_in_time'] = movie['start_sec'].astype('datetime64[s]').dt.time
movie['end_time_in_time'] = movie['End_time'].astype('datetime64[s]').dt.time


'''
from datetime import datetime

format = '%Y-%m-%d %H:%M %p'
my_date = datetime.strptime(str(new), format)

new2 =  pd.to_datetime(new, format = '%H:%M %p')

new3 = pd.to_datetime(results['start_sec'], unit = 's')


import time    
new4 = time.strftime('%H:%M:%S %p', time.gmtime(results['start_sec']))


new_5 =  pd.to_datetime(results['end_time_in_time'], format='%H:%M:%S.%f')

temp =  pd.to_datetime(results['end_time_in_time'], format='%H:%M:%S')


import time
timevalue_24hour = "20:10:10"
t = time.strptime(timevalue_24hour, "%H:%M:%S")
timevalue_12hour = time.strftime( "%I:%M:%S %p", t )

'''