'''
Created on Sep 29, 2016

@author: Administrator
'''
import os
print os.path.abspath("C:\Users\Administrator\git\pythonLearn\base")
print "jjjj".replace('old', 'new')
nTimes = 0
i = 0
while nTimes < 10:
    for i in [2,3,4]:
        print i
        if i == 3 :
            break
    print "nTimes = ",nTimes
    nTimes += 1