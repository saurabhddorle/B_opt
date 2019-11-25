# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:39:57 2019

@author: sdorle
"""

# Connecting to SQL server
import pyodbc 
import pandas as pd
import numpy as np

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=192.168.1.26;"
                        "Database=MODB@9SEP;"
                        "uid=sdorle;pwd=sdd@123") 


query = '''select
        ssd.air_date,
        ssd.content_duration_sec,
        ssd.promo_duration_sec,
        ssd.ad_duration_sec,
        ssd.content_start_time,
        ssd.content_end_time,
        ss.channel_id,
        rs.slot_id,
        rs.slot_desc,
        rs.dow_id,
        rs.dow_code,
        rct.content_tape_id,
        rct.content_id,
        rct.tape_name,
        rct.tape_duration_sec,
        rc.content_name,
        det.content_tape_detail_id,
        det.content_tape_id,
        det.content_tape_detail_name,
        det.tape_duration_sec,
        det.part_no,
        det.segment_no,
        det.tape_id
        from
        sch_schedule_detail ssd
        inner join sch_schedule ss on ssd.schedule_version_id = ss.final_schedule_version_id
        inner join ref_slot rs on ssd.slot_id = rs.slot_id
        inner join ref_content_tape rct on ssd.content_tape_id = rct.content_tape_id
        inner join ref_content rc on rct.content_id = rc.content_id
        left join ref_content_tape_detail det on ssd.content_tape_id = det.content_tape_id
        where ss.plan_id = 1015 and ssd.content_tape_id <> -1
        order by air_date, content_start_time, content_tape_detail_id'''
        
    
temp = pd.read_sql_query(query, cnxn)
