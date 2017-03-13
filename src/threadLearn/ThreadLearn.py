'''
Created on Mar 9, 2017

@author: taoqsun
'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time


GET_BRANCH_TIME_SLICE = 2

class ScriptsBranchsThread(threading.Thread):
    
    def __init__(self, time_slice):
        print "enter here."
        threading.Thread.__init__(self)
        self.time_slice = time_slice
        self.threadState = True
    
    def run(self):
        start_time = time.time()
        while self.threadState:
            if (time.time() - start_time) >= self.time_slice :
                start_time = time.time()
                print "thread is ..... ",time.time()
    def stop(self):            
        self.threadState = False
        
class ClientTATimer():
    """ create a timer to manager the all full run jenkins job
    """
    
    
    def __init__(self):
        """ init some parameters
        """        
        self.scriptsBranchsThread = ScriptsBranchsThread(GET_BRANCH_TIME_SLICE)
        
        self.scriptsBranchsThread.start()
    
    def run(self):
        """ the enter of the clientTATimer
        """
        print "start run 1..."
        job_run_time_and_date = time.time()
        while time.time() - job_run_time_and_date < 5:
            if time.time() % 2 == 2:
                print time.time()
        else:
            print "the run time more than one day,so the job end."
            self.scriptsBranchsThread.stop()

if __name__ == '__main__':
    testTA = ClientTATimer()
    testTA.run()