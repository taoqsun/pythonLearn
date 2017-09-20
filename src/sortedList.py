'''
Created on Feb 15, 2017

@author: sky
'''
from collections import namedtuple
import datetime
import time

RequiredMachineCount = namedtuple('RequiredMachineCount', ['win_at_least','win_at_best'])
reDict = {}
# for indexT in range(10):
#     resT = RequiredMachineCount(win_at_least=indexT,win_at_best=indexT+1)
#     reDict[indexT] = resT
print reDict
reDict[0] = RequiredMachineCount(win_at_least='14:03:53', win_at_best='14:01:54')
reDict[2]= RequiredMachineCount(win_at_least='14:02:53', win_at_best='14:02:54')
valueT = reDict.values()
print reDict

# x = time.strptime(,'%H:%M:%S')
print sorted(valueT,key=lambda x:time.strptime(x.win_at_least,'%H:%M:%S'))

curDict = {1:"1",2:"2",-1:"-1"}
curList = curDict.values()
curInt = []
for item in curDict.values():
    curInt.append(int(item))
print curInt
print curInt.sort()
print curInt
print sorted(curDict.values())
print sorted(curDict.keys())

listTemp = [0,3,5,1,4]
print sorted(listTemp)