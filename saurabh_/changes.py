# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 18:47:23 2019

@author: sdorle
"""

# BO_break_per_day
movie['break_min'] = 0
        
        # Total breaks duration
        total_break_per_hr_2 = (movie['AD_DURATION'].iat[0] + movie['PROMO_DURATION'].iat[0]) / 60
        
        try:
            movie_with_break = break_per_movie(movie, hours_dict, total_break_per_hr_2)
            final_2 = final_2.append(movie_with_break)
            del movie, movie_with_break

        except:
            print("\nError for placing breaks in Movie content_tape_id:", movie['content_tape_id'].iloc[0])
            #print("\n : ",sys.exc_info()[0])

###################################################            
# BO_break_per_movie

# Pass parameters to function 
total_break_per_hour

# Add in if condition in place of 840
total_break_per_hour


# Removing breaks at the end segment
if movie_1['break_min'].iloc[-1] != 0:
    # available indexes to place breaks
    available_index = movie_1.index[movie_1['break_min'] == 0].tolist()
    movie_1['break_min'].iloc[available_index[-1]] =  movie_1['break_min'].iloc[-1]
    
    movie_1['break_min'].iloc[-1] = 0
    
    # upatign time after palcing break
    movie_1 = time_update.start_time_update(movie_1)
    movie_1 = time_update.end_time_update(movie_1) 
    
###################################################   
# fun1 get_break_dur
# add at the end of function

    last_hr = df['Time_format'].iloc[-1]
    if last_hr.minute == 0:
         hours_dict[hours[1]] = 0

##################################################         
# bo_break_model_main
# save file of missing segments
np.savetxt("output_results\\Missing_Segments_" + str(plan_id_1) + ".csv", missing_segment_content_tape_ids, delimiter=",", fmt='%s', header = "Missing_segment_content_tape_id")


###############################################################################
# Round off break duration

results['break_in_min'] =  results['break_sec'].astype('datetime64[s]')
results['break_in_min'] =  pd.to_datetime(results['break_in_min'])
# Round off by second
new = results['break_in_min'].dt.round('10S').dt.time  
# Round off by minute
new = results['break_in_min'].dt.round('1min').dt.time  
results['break'] = new

##convert content_start_time into second
results['break_2'] = pd.to_timedelta(results['break'].astype(str))        
results['break_3'] = results['break_2'].dt.total_seconds()
###############################################################################

final['break_in_min'] =  final['break_min'].astype('datetime64[s]')
final['break_in_min'] =  pd.to_datetime(final['break_in_min'])
# Round off by second
new = final['break_in_min'].dt.round('10S').dt.time  
# Round off by minute
new = final['break_in_min'].dt.round('1min').dt.time  
final['break'] = new

##convert content_start_time into second
final['break_2'] = pd.to_timedelta(final['break'].astype(str))        
final['break_3'] = final['break_2'].dt.total_seconds()

final['break_min'] = final['break_3']

###################################################
data_2 = final
# storing content_tpae_ids of movie
content_tape_id = data_2.SCHEDULE_DETAIL_ID.unique()

# Hour wise Dictionary of Dataframes
tape_id_wise_group = dict(tuple(data_2.groupby('SCHEDULE_DETAIL_ID')))


final_2 = pd.DataFrame()

#content_tape_id = [12521]
#content_tape_id = [9140]
movie_count = 0
    
for i in content_tape_id:
    
    movie_count += 1
    
    movie = pd.DataFrame(tape_id_wise_group.get(i))
    movie = movie.reset_index()                     # Resetting the index
    movie.drop(['index'], axis=1, inplace = True)  
    
    movie = time_update.start_time_update(movie)
    movie = time_update.end_time_update(movie)   
    
    final_2 = final_2.append(movie)

final_2['start_time_in_time_2'] = final_2['start_sec'].astype('datetime64[s]').dt.time
final_2['end_time_in_time_2'] = final_2['End_time'].astype('datetime64[s]').dt.time



final_2.drop(columns=['break_in_min', 'break', 'break_2', 'break_3'], inplace = True)

