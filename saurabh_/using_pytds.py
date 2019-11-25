# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:38:24 2019

@author: sdorle
"""

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


arg = [tuple(x) for y,x in movie.iterrows()]
tvp = pytds.TableValuedParam(type_name='dbo.temp_sch_schedule_detail_fpc_test',rows= arg)
engine.execute('EXEC INSERT_FCT_TEST %s', (tvp,))




''' https://stackoverflow.com/questions/50141058/how-to-call-stored-procedure-with-sqlalchemy-that-requires-a-user-defined-type-t '''


''' https://hugoworld.wordpress.com/2019/01/06/slow-python-insert-performance-into-microsoft-sql-server/'''