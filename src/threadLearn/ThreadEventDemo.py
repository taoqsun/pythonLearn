'''
Created on Apr 25, 2017

@author: Administrator
'''
import threading
import time

listTemp = []

class threadClass1(threading.Thread):
#     listTemp = []
    def __init__(self, name, event):
        threading.Thread.__init__(self)
        self.name = name
        self.event = event
    
    def insertData(self,numb):
        self.event.clear()
        print time.ctime(time.time()) ,"befort sort = ",listTemp
        listTemp.append(numb)
        listTemp.sort()
        print time.ctime(time.time()) ,"after sort = ",listTemp
        self.event.set()
    
    def run(self):
        while True:
            print time.ctime(time.time()) ,"insert run listTemp = ",listTemp
            self.insertData(1)
    
class threadClass2(threading.Thread):
    def __init__(self, name, event):
        threading.Thread.__init__(self)
        self.name = name
        self.event = event
    
    def waitTime(self,loopTimes):
        self.event.clear()
        print time.ctime(time.time()) ," befort wait = ",listTemp
        for indes in range(loopTimes):
            print time.ctime(time.time()) ," wait = 1 seconds"
            time.sleep(1)
#             if not self.event.isSet():
#                 self.event.set()
#                 return loopTimes - indes -1
#         print time.ctime(time.time()) ," after wait = ",listTemp
     
    def run(self):
        while True:
            print time.ctime(time.time()) ,"waitTime run listTemp = ",listTemp
            self.waitTime(1)
           
class threadMain(threading.Thread):
    def __init__(self, name, event):
        threading.Thread.__init__(self)
        self.event = event
        self.thread1 = threadClass1("threadClass1",self.event)
        self.thread2 = threadClass2("threadClass2",self.event)
        self.thread1.run()
        self.thread2.run()
        
def main():
    event = threading.Event()
    threadMain1 = threadMain("threadMain",event)
    threadMain1.start()
    
main()