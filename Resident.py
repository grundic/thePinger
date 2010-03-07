#!/usr/bin/python
from multiprocessing import Pool
from time import sleep
from datetime import datetime


#----------------------------------------------------------------------------------------------------------
def resident(function, data, args=[], procCount=10):
    pool = Pool(processes=procCount)
        
    while True:
        start = datetime.now()
        data.result = pool.map(function, args)
        data.pingtime = str(datetime.now() - start)
        sleep(1)

