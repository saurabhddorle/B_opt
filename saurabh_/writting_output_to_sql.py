# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:39:03 2019

@author: sdorle
"""
import sys
import sqlalchemy 
import pyodbc 

engine = sqlalchemy.create_engine("mssql+pyodbc://sdorle:sdd@123@DATA_SCIENCE") 
results.to_sql(name ='BO_test_2', con = engine, if_exists = 'append', index = False)


###################################################################################
# Using Function

def write_to_db(result):
    
    try:
        engine = sqlalchemy.create_engine("mssql+pyodbc://sdorle:sdd@123@DATA_SCIENCE") 
        result.to_sql(name ='BO_test_2', con = engine, if_exists = 'replace', index = False)
        print("\n Successfully updated in Database")        
        
    except:
        print("Error in DbInterface : ",sys.exc_info()[0])
        
    #finally:
     #   print("\n DONE")
        

write_to_db(results)


# =============================================================================
# Row_wise inserting
# =============================================================================

    
import pandas as pd
import pyodbc

################## For single row ################

cnxn = pyodbc.connect("DSN=DATA_SCIENCE", UID = "sdorle", PWD = "sdd@123")
cursor = cnxn.cursor()

cursor.execute("insert into BO_test_4(slot_id) values ('9')")
cnxn.commit()


################# For all rows ###################

# creating column list for insertion
cols = ",".join([i for i in results.columns.tolist()])

# Insert DataFrame records one by one.
for i,row in results.iterrows():
    sql = "INSERT INTO BO_test_4 (" +cols + ") VALUES (" + "?,"*(len(row)-1) + "?)"
    cursor.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    cnxn.commit()
    
    

# =============================================================================
# Using TABLE VALUED PARAMETER ( inserting full table at a time) Using procedure
# =============================================================================


import pandas as pd
import pytds
from pytds import login
import sqlalchemy as sa
from sqlalchemy import create_engine
import sqlalchemy_pytds


def connect():
    return pytds.connect(dsn='192.168.1.26', database = 'MODB@9SEP', user = 'sdorle', password = 'sdd@123', autocommit=True)#, auth=login.SspiAuth())

engine = sa.create_engine('mssql+pytds://MODB_9SEP', creator=connect)
conn = engine.raw_connection()

# Storing rows of dataframe in arg variable
arg = [tuple(x) for y,x in df.iterrows()] # 
# creating table valued parameter 
tvp = pytds.TableValuedParam(type_name='dbo.temp_sch_schedule_detail_fpc_test',rows= arg) # 'dbo.temp_sch_schedule_detail_fpc_test' is dbo tye defined in procedure
# calling procedure and passing table valued parameter
engine.execute('EXEC INSERT_FCT_TEST %s', (tvp,)) # 'INSERT_FCT_TEST' Procedure name




