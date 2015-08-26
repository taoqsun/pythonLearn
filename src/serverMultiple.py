'''
Created on Aug 19, 2015

@author: sky
'''
import socket
import sys
from thread import *
import subprocess
import threading
import errno
import time
 
HOST = '10.224.74.220'   # Symbolic name meaning all available interfaces
PORT = 52000 # Arbitrary non-privileged port
global event 
threadLock = threading.Lock()
event      = threading.Event()
threadList=[]
threadName=[] 

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
# s.setblocking(1)
# s.settimeout(10)
print 'Socket now listening'
class myThread (threading.Thread):
    def __init__(self, threadID, name,connectObj):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn=connectObj
        self.isFlag=False
    def run11(self):
        #Sending message to connected client
        
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            try:
                #Receiving from client
                data = self.conn.recv(1024)
                print "receive data:",data
                if not len(data):break
                
                if data == 'start clear log':
                    print "start clear log"
                    print "thread name",self.name
                    self.conn.sendall('clear log') 
                    break
                
                if data == 'run':
                    filepath="C:/Users/Administrator/Desktop/copycaseFile 2.bat"
                    print "start copy case and zipFile to remote"
                    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
                    stdout, stderr = p.communicate()
                    if p.returncode == 0:
                        print " copy case and zipFile to remote success"
                        self.conn.sendall('copy case and zipFile to remote computer success')
                        event.set()
                        self.isFlag=True
                        break
                    
                if data =='clear log and code success':
                    print "reset event"
                    event.clear()
                    self.isFlag=False
                    break
                
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK: 
                    print 'EWOULDBLOCK'
                    time.sleep(1)           # short delay, no tight loops
                else:
                    print e
                    break


#now keep talking with the client
while True and len(threadList) <= 3:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        threadTemp=myThread(addr[0],'threadName'+addr[0],conn)
#         print "threadList length===",len(threadList)
        while True:
            try:
                #Receiving from client
                data = conn.recv(1024)
                print "receive data:",data
                if not len(data):break
                
                if data == 'start clear log':
                    print "start clear log"
                    conn.sendall('clear log') 
                    break
                
                if data == 'run':
                    filepath="C:/Users/Administrator/Desktop/copycaseFile 2.bat"
                    print "start copy case and zipFile to remote"
                    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
                    stdout, stderr = p.communicate()
                    if p.returncode == 0:
                        print " copy case and zipFile to remote success"
                        conn.sendall('copy case and zipFile to remote computer success')
                        event.set()
                        isFlag=True
                        break
                    
                if data =='clear log and code success':
                    print "reset event"
                    event.clear()
                    isFlag=False
                    break
                    
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK: 
                    print 'EWOULDBLOCK'
                    time.sleep(1)           # short delay, no tight loops
                else:
                    print e
                    break
        conn.close()        
    except KeyboardInterrupt:
        print "thread stop "
        sys.exit(0)
        
s.close()        
        
        
        
#         for temp in threadList:
#             if temp.getName() == 'threadName10.224.74.181':
#                     temp.runScript()
#                     
#         #             print "event.isSet()===",event.isSet()
#             
#             if event.isSet() == True and temp.getName() != 'threadName10.224.74.181':
#                     temp.runScript()   
            
    
#     except KeyboardInterrupt:
#         print "thread stop "
#         sys.exit(0)
        
 
        



    
 
