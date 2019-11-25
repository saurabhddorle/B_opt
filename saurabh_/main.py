# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 15:18:26 2019

@author: sdorle
"""


import time
start_time = time.clock()

from bo_model_main import *

def model():    
    results = Run_bo_model(1015)

    
model()

#print(time.clock() - start_time, "seconds")   
