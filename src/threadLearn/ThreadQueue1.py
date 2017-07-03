'''
Created on Apr 26, 2017

@author: Administrator
'''
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time
import Queue

SHARE_Q = Queue.Queue()  
_WORKER_THREAD_NUM = 3   

class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func

    def run(self) :
        self.func()

def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        item = SHARE_Q.get() 
        print "Processing : ", item
        time.sleep(1)

def main() :
    global SHARE_Q
    threads = []
    for task in xrange(5) : 
        SHARE_Q.put(task)
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads :
        thread.join()

if __name__ == '__main__':
    main()