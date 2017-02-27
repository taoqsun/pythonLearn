# -*- coding: utf-8 -*-
'''
Created on 2015��9��26��

@author: Administrator
'''
import time
from datetime import datetime


TIME_FORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S'

# monthCurr =int( time.strftime('%m',time.localtime(time.time())))-1
print time.localtime()
print time.time()
print datetime.now()
# print monthCurr
# print monthCurr2
CurrentTime = time.strftime(TIME_FORMAT_DEFAULT,time.localtime(time.time()))
CurrentTime = datetime.strptime(CurrentTime,TIME_FORMAT_DEFAULT)
time.sleep(1)
job_run_time = datetime.strptime(time.strftime(TIME_FORMAT_DEFAULT,time.localtime(time.time())),TIME_FORMAT_DEFAULT)
print CurrentTime,job_run_time
# job_run_time = time.strftime(TIME_FORMAT_DEFAULT,time.localtime(time.time()))
# print "job_run_time =  %s ,CurrentTime =  %s"%(job_run_time,CurrentTime)

print (job_run_time - CurrentTime).seconds