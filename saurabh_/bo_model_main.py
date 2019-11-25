# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:14:15 2019

@author: sdorle
"""

#import time
#start_time = time.clock()
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import sys
import sqlalchemy 
import pyodbc 
from pathlib import Path
import os
from get_break_schedule_ import *
from bo_break_per_day import single_day_break
from fun1 import *



    
def Run_bo_model(plan_id_1):
    #plan_id_1 = 1021
    ##### Importing one day schedule ###########
    dataset = get_break_schedule(plan_id_1)
    #dataset = plan_id_1
    #dataset = pd.read_excel('data\\schedule_1067_excel.xlsx', encoding='latin1')#one_month_ordered.csv
    dataset = dataset[['SCHEDULE_DETAIL_ID', 'CONTENT_TAPE_DETAIL_ID', 'AIR_DATE', 'CONTENT_TAPE_ID', 'CONTENT_TAPE_ID_1', 'CONTENT_START_TIME',
                       'CONTENT_END_TIME', 'SEGMENT_DURATION_SEC', 'SEGMENT_NO', 'DOW_ID', 'SLOT_ID', 'AD_DURATION', 'PROMO_DURATION']]
    
    # Converting to datetime format
    dataset['AIR_DATE'] = pd.to_datetime(dataset['AIR_DATE']).dt.date
    
    ###############################################################################
    # Selecting single day from schedule
    date_wise_group = dict(tuple(dataset.groupby('AIR_DATE')))
    
    # storing content_tpae_ids of movie
    air_dates = dataset.AIR_DATE.unique()
    
    final = pd.DataFrame()
    non_break_movie = pd.DataFrame()
    
    missing_segment_content_tape_ids = []
    
    for d in range(0, len(air_dates)):# len(air_dates)
        
        day = pd.DataFrame(date_wise_group.get(air_dates[d]))
        print("\n Scheduling the break for Date: ", air_dates[d])
        
        day = day.reset_index()
        day.drop(['index'], axis=1, inplace = True)
        
        ###############################################################################
        # Removing movies where segments not available
        content_tape_id1 = day.CONTENT_TAPE_ID.unique()
        
        index = day['CONTENT_TAPE_ID'].index[day['CONTENT_TAPE_ID'].apply(np.isnan)]
        
        df_index = day.index.values.tolist()
        rem_index = [df_index.index(i) for i in index]
       
        for idx in rem_index:
            #print("\n#### Segments not available for content_tape_id :", day['CONTENT_TAPE_ID_1'].iloc[idx] )
            missing_segment_content_tape_ids.append(day['CONTENT_TAPE_ID_1'].iloc[idx])
        
        for idx in rem_index:
            day = day.drop(index = idx)         
            
    
        
        ###############################################################################
        ##convert content_start_time into second
        day['Start_time'] = pd.to_timedelta(day['CONTENT_START_TIME'].astype(str))        
        day['start_seconds'] = day['Start_time'].dt.total_seconds()
        
        ##convert content_end_time into second
        day['End_time'] = pd.to_timedelta(day['CONTENT_END_TIME'].astype(str))
        day['end_sec'] = day['End_time'].dt.total_seconds()
        
        
        ## Get Month and Day from Date 
        day['AIR_DATE'] = pd.to_datetime(day['AIR_DATE'])
        
        day['Month'],day['Day'] = day.AIR_DATE.dt.month, day.AIR_DATE.dt.day
        #day['Year'] = day.AIR_DATE.dt.year
        #day['week_name'] = day.air_date.dt.weekday_name
        
        ###############################################################################
        grp = dict(tuple(day.groupby('CONTENT_TAPE_ID')))
        
        # New Dataframe for storing all start time in seconds for all sengments
        final_ = pd.DataFrame()
        
        #content_tape_id = list(day['content_tape_id']).unique() 
        content_tape_id_list = day.CONTENT_TAPE_ID.unique()
        
        day['Start_seconds'] = pd.Series()
        day['Start_seconds'] = 0
        # Calculating start time of segments based on movie start time
        for i in content_tape_id_list:
            #final = pd.DataFrame()
            tmp = pd.DataFrame(grp.get(i))
            tmp = tmp.reset_index()
            tmp.drop(['index'], axis=1, inplace = True)
            
            tmp['Start_seconds'] = tmp.at[0, 'start_seconds']
            for i in range(1, len(tmp)):
                tmp.at[i,'Start_seconds'] = tmp.at[i-1,'Start_seconds'] + tmp.at[i-1,'SEGMENT_DURATION_SEC']
                
            final_ = final_.append(tmp, ignore_index = True)#, sort = True)        
            del tmp
            
        # Converting to hour format
        final_['hour'] = (final_['Start_seconds'] / 3600).apply(np.floor)
        
        #######################################################################
        # Renaming the columns as per requirement
        
        final_.rename(columns={"DOW_ID": "Dow_id", "SEGMENT_DURATION_SEC": "tape_duration_sec",
                               "CONTENT_TAPE_ID": "content_tape_id", "SEGMENT_NO": "segment_no",
                               "AIR_DATE": "air_date", "SLOT_ID": "slot_id"}, inplace = True)
        # Keeping only required columns
        data = final_[['air_date', 'SCHEDULE_DETAIL_ID', 'CONTENT_TAPE_DETAIL_ID', 'content_tape_id', 
                       'tape_duration_sec', 'segment_no', 'Start_seconds', 'end_sec', 'Month', 
                       'Day', 'Dow_id', 'hour', 'slot_id', 'AD_DURATION', 'PROMO_DURATION']] 
        del final_
        
        # Segment reach prediction
        predicted = reach_prediction(data)
        del data
        # break schedule
        results = single_day_break(predicted)
        del predicted
        
        # Storing results for single day in dataframe
        final = final.append(results[0])
        if len(results[1]) > 0:
            non_break_movie = non_break_movie.append((results[1]))
        del results
    
    ###########################################################################
    # Adding promo duration column
    final['promo_sec'] = 0
    # renaming the columns
    final.rename(columns={"break_min": "ad_duration_sec",
                          "SCHEDULE_DETAIL_ID": "schedule_detail_id", 
                          "CONTENT_TAPE_DETAIL_ID": "content_tape_detail_id",
                          "tape_duration_sec": "segment_duration_sec",
                          "promo_sec": "promo_duration_sec"}, inplace = True)
       
    # Keeping only required columns    
    final_2 = final[['schedule_detail_id', 'content_tape_detail_id', 
                     'segment_duration_sec', 'ad_duration_sec', 'promo_duration_sec', 'slot_id', 'air_date']]             
    
    # Content tape ids of missing segment movies
    print("\n ################ Content_tape_ids of Movies with missing segments ################")
    print("\n ", missing_segment_content_tape_ids)
    
    # Printing the results
    print("\n ############################################## Result #################################################### \n")           
    print(final_2)
    
    ########### Saving output file to specified directory ###################### Filw ith all columns #############
    try:
        os.mkdir('output_results/Schedule_id_'+str(plan_id_1))
    except:
        print("\nDir exist")
    p = Path('output_results/Schedule_id_' + str(plan_id_1) + "/")
    final.to_csv(Path(p, 'Plan_id_' + str(plan_id_1) + '.csv'), index=False)
    
    np.savetxt("output_results\\Schedule_id_"+ str(plan_id_1) + "\\Missing_Segments_" + str(plan_id_1) + ".csv", missing_segment_content_tape_ids, delimiter=",", fmt='%s', header = "Missing_segment_content_tape_id")
    
    # Saving movies where breaks are not placed
    non_break_movie.to_csv(Path(p, 'Movies_withoud_break' + str(plan_id_1) + '.csv'), index=False)
    #write_to_db(final_2)
    
    
    print("\n \n ################### Process Complete ######################## \n\n")
           
    return final_2
    #print(time.clock() - start_time, "seconds")   
        
    #final.to_csv("one_month_results_column.csv", index = False)
    

#def write_to_db(result):
    
#    try:
#        engine = sqlalchemy.create_engine("mssql+pyodbc://sdorle:sdd@123@DATA_SCIENCE") 
#        result.to_sql(name ='BO_test_2', con = engine, if_exists = 'replace', index = False)
#        print("\n Successfully updated in Database")        
#        
#    except:
#        print("Error in DbInterface : ",sys.exc_info()[0])
        
#write_to_db(final_2)
    

