#!/usr/bin/python
import socket
import subprocess
import sys

HOST='10.224.74.220'
# HOST='127.0.0.1'
PORT=52000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
s.connect((HOST,PORT))       #要连接的IP与端口

while True:
    try:
        
        cmd=raw_input("Please input cmd:")       #与人交互，输入命令
        s.sendall(cmd)      #把命令发送给对端
        data=s.recv(1024)   #把接收的数据定义为变量
        print data         #输出变量
        if (data=='copy case and zipFile to remote computer success'):
                print "start copy case and zipFile to local" 
                filepath="C:/Users/Administrator/Desktop/copycaseFile.bat"
                p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
                stdout, stderr = p.communicate()
                if p.returncode == 0:
                    print "copy case and zipFile to local success"
                    p.kill()
        
    except :
        print "程序被强行停止！ " 
        sys.exit(0)
#                     break
s.close()   #关闭连接
