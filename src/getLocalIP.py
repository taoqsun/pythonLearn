'''
Created on Oct 16, 2015

@author: sky
'''
import socket
def __getlocalIP():
        try:
            SCOKET=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            SCOKET.connect(('8.8.8.8',80))
            (addr,port) = SCOKET.getsockname()
            SCOKET.close()
            return addr
        except socket.error:
            return "127.0.0.1"

print  __getlocalIP()