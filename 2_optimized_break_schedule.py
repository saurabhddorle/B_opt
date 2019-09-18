# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:50:50 2019

@author: sdorle
"""



from break_count import get_extra_break_count, get_add_break_count
from break_remove_time_update import remove_break

extra_break_count = get_extra_break_count(final)

while extra_break_count != 0:
    final = remove_break(final)
    extra_break_count = get_extra_break_count(final)
    


from add_break_time_update import add_break

add_break_count = get_add_break_count(final)

final2 = add_break(final)



# Converting seconds to actual datetime format
final2['start_time'] = pd.to_datetime(final2['start_sec'], unit = 's').dt.time

#final2.to_csv("17-09-2019_break_add_row_wise_all_movies_final_with_time_12min_break.csv", index = False)