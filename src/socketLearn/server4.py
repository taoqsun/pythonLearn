'''
Created on Aug 19, 2015

@author: sky
'''
#!/usr/bin/python
 
# Import all from module socket
from socket import *
#Importing all from thread
from thread import *
import subprocess
# Defining server address and port
host = '10.224.74.181'  #'localhost' or '127.0.0.1' or '' are all same
port = 52000 #Use port > 1024, below it all are reserved
 
#Creating socket object
sock = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(5) #5 denotes the number of clients can queue
# sock.settimeout(3)
def clientthread(conn):
#infinite loop so that function do not terminate and thread do not end.
#     conn, addr = sock.accept()
    data=''
    while True:
#Sending message to connected client
#         conn.send('Hi! I am server\n') #send only takes string
#Receiving from client
#         conn.setTimeout(3)

        data = conn.recv(1024) # 1024 stands for bytes of data to be received
        conn.settimeout(3)
        print data
        if data == 'run':
            filepath="C:/Users/Administrator/Desktop/copycaseFile 2.bat"
            p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
            stdout, stderr = p.communicate()
            print p.returncode # is 0 if success
            if p.returncode == 0:
                conn.sendall('0')
                print "send 0" 
        else:
            conn.send('1')
            print "send 1"
threadNum=0
threadList=[] 
while threadNum < 4:
#Accepting incoming connections
    conn, addr = sock.accept()
    print'Connected by',addr
#Creating new thread. Calling clientthread function for this function and passing conn as argument.
    threadList.append(start_new_thread(clientthread,(conn,))) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    threadNum=threadNum+1
    
conn.close()
sock.close()