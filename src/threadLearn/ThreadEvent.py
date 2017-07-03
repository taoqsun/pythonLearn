'''
Created on Apr 25, 2017

@author: Administrator
'''
import threading
import time

class TestThread(threading.Thread):
    def __init__(self, name, event):
        super(TestThread, self).__init__()
        self.name = name
        self.event = event
    
    def run(self):
        print 'Thread: ', self.name, ' start at:', time.ctime(time.time())
        self.event.wait()
        print 'Thread: ', self.name, ' finish at:', time.ctime(time.time())
        
def main():
    event = threading.Event()
    threads = []
    for i in range(1, 5):
        threads.append(TestThread(str(i), event))
    print 'main thread start at: ', time.ctime(time.time())
    print event.isSet()
    event.clear()
    for thread in threads:
        thread.start()
    print 'sleep 5 seconds....... \n'
    time.sleep(5)
    print 'now awake other threads....\n'
    for thread in threads:
        print thread.getName(), " = " ,event.isSet()
#     event.set()   

main()