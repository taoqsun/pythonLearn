'''
Created on Aug 15, 2017

@author: Administrator
'''
import os,subprocess
try:
#     devnull = open(os.devnull, 'wb') #python >= 2.4
#     p1 = subprocess.call("C:\Cisco_WebEx_Add-On.exe", shell=False,
#                           stdout=subprocess.PIPE, stderr=devnull)
    process = subprocess.Popen(r"C:\Cisco_WebEx_Add-On.exe", shell=True, stdout=subprocess.PIPE)
    ret1=process.wait()
#     p1 = subprocess.call(r"C:\Cisco_WebEx_Add-On.exe", stdin=None, stdout=None, stderr=devnull, shell=False)
#     p1=subprocess.Popen(r"C:\Cisco_WebEx_Add-On.exe")
#     print p1.poll()
#     ret1=p1.wait()
    process.kill()
    if ret1 != 0:
        downloadStatus = False
except Exception,e:
    print "install add on error : %s" % str(e)