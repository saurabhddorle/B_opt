# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:32:42 2019

@author: sdorle
"""

def low_reach(df):
    # Sorting based on reach values  
    res = df.sort_values(['Reach'], ascending=[1])
    res = res.index.tolist()

    return res
