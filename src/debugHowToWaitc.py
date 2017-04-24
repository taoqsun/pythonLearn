'''
Created on Apr 24, 2017

@author: sky
'''
import time

def _howToWait(totalWaitTime,sizeList = [600,60,5,1]):
        loopList = []
        for indexTemp in range(len(sizeList)):
            loopTimes = totalWaitTime / sizeList[indexTemp]
            reminder = totalWaitTime % sizeList[indexTemp]
            if loopTimes >= 1 and reminder == 0 :
                if sizeList[indexTemp] == 1 :
                    loopList.append(loopTimes)
                else:
                    loopList.append(loopTimes - 1 )
                totalWaitTime = sizeList[indexTemp]
                continue
            elif loopTimes != 0 and reminder != 0:
                loopList.append(loopTimes)
                totalWaitTime = totalWaitTime - (loopTimes * sizeList[indexTemp])
                continue
            else:
                loopList.append(0)      
        for indexLoopList in range(len(loopList)):
            indexT = 0
            if len(loopList) != 0 :
                if  loopList[indexLoopList] == 0:
                    continue
                for indexT in range(loopList[indexLoopList]):
                    print  "wait time :%s s ...... " % str(sizeList[indexLoopList])
                    time.sleep(sizeList[indexLoopList])


totalWaitTime = 29
_howToWait(totalWaitTime)