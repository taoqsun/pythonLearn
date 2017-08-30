# -*- coding: utf-8 -*-
'''
Created on 2015��9��26��

@author: Administrator
'''
import time
from datetime import datetime as datetime2
import datetime

TIME_FORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S'

# monthCurr =int( time.strftime('%m',time.localtime(time.time())))-1
# print time.localtime()
# print time.time()
# print datetime.now()
staticTime = datetime2.now()
print staticTime
# print monthCurr
# print monthCurr2
# CurrentTime = time.strftime(TIME_FORMAT_DEFAULT,time.localtime(time.time()))
# CurrentTime = datetime.strptime(CurrentTime,TIME_FORMAT_DEFAULT)
# time.sleep(1)
job_run_time = datetime2.strptime("2017-02-26 11:16:06",TIME_FORMAT_DEFAULT)
job_run_time2 = datetime2.strptime("2017-02-28 11:16:07",TIME_FORMAT_DEFAULT)
print job_run_time,job_run_time2 
# print CurrentTime,job_run_time
# job_run_time = time.strftime(TIME_FORMAT_DEFAULT,time.localtime(time.time()))
# print "job_run_time =  %s ,CurrentTime =  %s"%(job_run_time,CurrentTime)

# print (job_run_time - CurrentTime).seconds
# time.sleep(1)
print (job_run_time - staticTime).seconds
print "job_run_time + 2 = ",job_run_time + datetime.timedelta(0,2)
print "job_run_time + 200 = ",job_run_time + datetime.timedelta(0,200)
print (job_run_time2 - job_run_time).seconds


start_time = time.time()
print start_time
# your code
time.sleep(0)
elapsed_time = time.time() - start_time
print elapsed_time
if time.time() - start_time >= 1:
    print "elapsed_time = ",elapsed_time
