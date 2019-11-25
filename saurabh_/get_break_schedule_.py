# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:34:33 2019

@author: sdorle
"""


import pyodbc 
import pandas as pd
import numpy as np

def get_break_schedule(plan_id):
    
    #cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
     #                   "Server=192.168.1.26;"
      #                  "Database=MODB@9SEP;"
      #                  "uid=sdorle;pwd=sdd@123") 


    cnxn = pyodbc.connect(dsn='MODB_15NOV', uid='sdorle', pwd='sdd@123')						

    #plan_id = 1015    
    sqlExecSP_="{call GET_BREAK_SEGMENT_DATA_BY_PLAN_ID (?)}"
    data2 = pd.read_sql(sqlExecSP_, cnxn, params=[plan_id]) 
    
    return data2





