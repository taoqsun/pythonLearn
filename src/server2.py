'''
Created on Aug 19, 2015

@author: taoqsun
'''
import socket
import sys
from thread import *
import subprocess
import threading
import errno
import time
import Queue
  
HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
PORT = 52000 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(5)
print 'Socket now listening'
q = Queue.Queue(maxsize = 10)
class myThread (threading.Thread):
    global testFlag
    def __init__(self, threadID, name,connectObj,event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn=connectObj
        self.event = event
        
    def run(self):
        #Sending message to connected client
        #infinite loop so that function do not terminate and thread do not end.
        
        while True:
            try:
                #Receiving from client
                data = self.conn.recv(1024)
                
                print "server receive data:%s,",data,self.getName()
                print "thread is alive",self.isAlive(),self.getName()
                if not len(data):break
                
                if data == 'connected success and wait start clear log':
                    event.wait()
                    print "start clear log",self.getName()
#                     print "thread is alive",self.isAlive()
                    self.conn.sendall('clear log') 
                
                if data == 'run':
#                     testFlag=False
#                     q.put_nowait(testFlag)
                    print 'start copy case and zipFile to remote computer',self.getName()
                    self.conn.sendall('copy case and zipFile to remote computer success')
                    q.put_nowait(False)
                    
                if data == 'copy case and zipFile to local success' :   
                    print 'event is set',self.getName()
                    event.set()
                    print "thread is alive",self.isAlive()
                        
                        
                if data =='clear log and old code success':
#                     self.conn.sendall('clear log and old code success')
                    print "reset event",self.getName()
#                     q.put_nowait(False)
                    event.clear()
                    
                if not q.empty() :
                    if q.get_nowait() == False:
#                         print 'testflag====',testFlag,self.getName()
                        self.conn.sendall('all is end')
                        print "thread is alive",self.isAlive()
                        print "send  all is end",self.getName()     
            
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK: 
                    print 'EWOULDBLOCK',self.getName() 
                    time.sleep(5)           # short delay, no tight loops
                else:
                    print e
                    break
                if not q.empty() :
                    if q.get_nowait() == False:
#                         print 'testflag====',testFlag,self.getName()
                        self.conn.sendall('all is end')
                        print "thread is alive",self.isAlive()
                        print "send  all is end",self.getName()

#now keep talking with the client
event=threading.Event()

while True:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        s.settimeout(20)
        threadTemp=myThread(addr[0],'threadName'+str(addr[1]),conn,event)
        threadTemp.start()
        
    except socket.error,KeyboardInterrupt:
        print "thread stop or time out "
#         sys.exit(0)
conn.close()
s.close()


    
 
