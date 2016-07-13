'''
Created on May 31, 2016

@author: sky
'''
import os
import sys
import time
import subprocess
from time import sleep
from _ast import While

def getCurrentScriptPath():
    curPath = sys.path[0]
    if os.path.isfile(curPath):
        curPath = os.path.dirname(curPath)
    return curPath

def cprint(log):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " -- " + str(log)

def __runMBJavaAPI(infoFile):
    os.environ["Path"] = os.environ["Path"] + "C:\client_mb_job"
    try:
        print "getCurrentScriptPath() ===>",getCurrentScriptPath()
        print "infoFile == >",infoFile
        time.sleep(10)
        javaCmd = r'java -cp %s;%s %s %s %s' % (getCurrentScriptPath(),'"C:\Program Files\Cisco Webex\MagicBoat\SDK\Java\MagicBoatSDK.jar"', '"AutoMBJob"', infoFile, '1')
        print "javaCmd ====> ",javaCmd
        ret = os.popen(javaCmd).readlines()
        print "return message == >",ret
        time.sleep(10)
    except Exception,e:
        print e
        
    return ret

def runSTAFCmd(stafCmd,timeOutValue = 30):
    try:
        print  "stafCmd  == >",stafCmd
#         ret = os.popen(stafCmd).readlines()
        p = subprocess.Popen(stafCmd, shell=True)        
        timeOut = 0
        ret = None
        while ret == None and timeOut <= timeOutValue:
            ret = p.poll()
            time.sleep(1)
            timeOut = timeOut + 1
        if timeOut > timeOutValue :
            print "runSTAFCmd : \"" + stafCmd +"\" time out ...."
        return ret
    except Exception,e:
        print  "error message:  ",e

def copyLocalFileToRemoteMachine(srcFile, dstFile, remoteIP):
    stafCmd = "staf local fs copy file %s tofile %s tomachine %s" % (srcFile, dstFile, remoteIP)
    print stafCmd
    try:
        ret = runSTAFCmd(stafCmd)
        if ret[2] == "\n":
            return True
        else:
            return False
    except Exception,e:
        print "error message:  ",e


# __runMBJavaAPI('"C:\client_mb_job\Mac_Python_iMagic_WebExClient.zip"')        
runSTAFCmd("staf local fs copy DIRECTORY \"C:\Program Files\Cisco Webex\MagicBoat\Lib\python_mac\iMagic\Mac_Python_iMagic_WebExClient/\" TODIRECTORY \"/Users/admin/Library/MagicBoat/Lib/python_mac/iMagic/Mac_Python_iMagic_WebExClient/\" TOMACHINE 10.224.73.176 RECURSE")

runSTAFCmd("staf 10.224.73.176 fs delete entry \"/Users/admin/Library/MagicBoat/Lib/python_mac/iMagic/Mac_Python_iMagic_WebExClient\" confirm recurse")

runSTAFCmd("staf 10.224.73.176 process start command \"python\"")
