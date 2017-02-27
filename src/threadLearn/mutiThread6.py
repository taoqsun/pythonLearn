'''
Created on Feb 14, 2017

@author: taoqsun
'''
from multiThread4 import DemoThread
from time import sleep

dt = DemoThread("name1")
timesTemp = 0
while timesTemp < 10:
    sleep(1)
    print dt.getName(),dt.getSelfList()
    timesTemp += 1