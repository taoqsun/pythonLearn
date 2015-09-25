'''
Created on Sep 25, 2015

@author: taoqsun
'''
import os
import time

def fdbg(log):
        path = os.path.dirname(__file__)
        index = path.rfind("handleMail")
        if(-1 != index):
            logpath = path[:index] + ".\Logs" 
            if(os.path.exists(logpath) == False):
                os.mkdir(logpath)
        else:
            print "Invalid Log file Path."
            return
            
        logfile = logpath + "/" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".txt"
        file_handle = open(logfile,"a+")
        file_handle.writelines(str(log) + "\n")
        file_handle.close()
