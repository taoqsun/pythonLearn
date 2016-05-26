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
 
HOST = '10.224.74.220'   # Symbolic name meaning all available interfaces
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
class myThread (threading.Thread):
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
                print "server receive data:",data
                
                if not len(data):break
                
                if data == 'connected success and wait start clear log':
                    event.wait()
                    print "start clear log"
                    self.conn.sendall('clear log') 
                
                if data == 'run':
                    filepath="C:/Users/Administrator/Desktop/copycaseFile 2.bat"
                    print "start copy case and zipFile to remote"
#                     self.conn.sendall('start copy case and zipFile to remote') 
                    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
                    stdout, stderr = p.communicate()
                    if p.returncode == 0:
                        print " copy case and zipFile to remote success"
                        self.conn.sendall('copy case and zipFile to remote computer success')
                        event.set()
                        p.kill()
                        
                if data =='clear log and old code success':
#                     self.conn.sendall('clear log and old code success')
                    print "reset event"
                    event.clear()
                    
            
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK: 
                    print 'EWOULDBLOCK'
                    time.sleep(1)           # short delay, no tight loops
                else:
                    print e
                    break

#now keep talking with the client
event=threading.Event()
while True:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        threadTemp=myThread(addr[0],'threadName'+addr[0],conn,event)
        threadTemp.start()
        
    except KeyboardInterrupt:
        print "thread stop "
        sys.exit(0)
conn.close()
s.close()


    
 
