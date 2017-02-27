'''
Created on Feb 14, 2017

@author: taoqsun
'''
from threading import Thread
import types
from time import sleep

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls] 
 
 
class DemoThread(Thread):
    __metaclass__ = Singleton
    def __init__(self, threadName):
        """Initializes thread"""
        
        Thread.__init__(self, name=threadName)
        self.listVariable = []
        # ensures that each vehicle waits for a green light
    def insertMessage(self,listTemp = []):
        if isinstance(listTemp,types.ListType):
            self.listVariable.extend(listTemp)
    
    def getSelfList(self):
        return self.listVariable



# dt = DemoThread("name1")
# print dt.getName()
# print "before == ",dt.getSelfList()
# sleep(2)
# dt.insertMessage(listTemp = [1,2,3])
# sleep(2)
# print "after == ",dt.getSelfList()
