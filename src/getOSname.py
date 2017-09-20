'''
Created on Oct 29, 2015

@author: sky
'''
import os
print os.name
import platform
print platform.system()
print platform.release()
if os.path.getsize("C:\\1.txt") != 0:
    print "you got it"