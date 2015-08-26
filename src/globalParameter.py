'''
Created on Aug 25, 2015

@author: sky
'''
#-*-coding: utf-8 -*-
import time
from threading import Thread
global timeout
timeout = False
def count():
    global timeout
    i = 0
    while(not timeout):
        print i, timeout
        time.sleep(0.2)
        i += 1
def timer():
    global timeout
    print timeout
    time.sleep(5)
    timeout = True

if __name__ == "__main__":
    tCounter = Thread(target = count)
    tTimer = Thread(target = timer)
    tTimer.start()
    tCounter.start()