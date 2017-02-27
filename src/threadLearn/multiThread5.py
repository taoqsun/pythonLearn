'''
Created on Feb 14, 2017

@author: taoqsun
'''
import time
from multiThread4 import DemoThread

dt2 = DemoThread("name2")
print "before == ",dt2.getName(),dt2.getSelfList()
time.sleep(2)
dt2.insertMessage(listTemp = [1,2,3])
time.sleep(2)
print "after == ",dt2.getName(),dt2.getSelfList()