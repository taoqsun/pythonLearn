#!/usr/bin/python
import socket
import os
import subprocess

HOST='127.0.0.1'
PORT=52000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
s.connect((HOST,PORT))       #要连接的IP与端口
while 1:
        s.sendall('connected success and wait start clear log')
        data=s.recv(1024)     #把接收的数据定义为变量
        print "client 11 receive====",data         #输出变量
        if (data== 'clear log'):
            print "start clear log and code"
#             filepath=". /Users/admin/Desktop/clearLog.sh"
#             p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
#             stdout, stderr = p.communicate()
#             if p.returncode == 0:
#                 print "clear log and code success"
            s.sendall("clear log and old code success") 
            
            
s.close()   #关闭连接
