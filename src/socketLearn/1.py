#!/usr/bin/python
import socket
import subprocess
import time

HOST='127.0.0.1'
PORT=52000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
s.connect((HOST,PORT))       #要连接的IP与端口
testF=False
while 1:
    s.sendall('')
    if not testF:
        cmd=raw_input("Please input cmd:")       #与人交互，输入命令
        s.sendall(cmd)      #把命令发送给对端
        testF=True
    data=s.recv(1024)   #把接收的数据定义为变量
    print data+'\r'         #输出变量
    if (data=='copy case and zipFile to remote computer success'):
            print "start copy case and zipFile to local" 
            time.sleep(2)
            print "copy case and zipFile to local success"
            s.sendall('copy case and zipFile to local success')
            continue
    if(data=='all is end'):
        testF=False    
#                     break
s.close()   #关闭连接
