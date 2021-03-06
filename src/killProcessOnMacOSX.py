'''
Created on Oct 13, 2015

@author: taoqsun
'''
import subprocess, signal
import os,sys

def iswindows():
    if os.name.startswith('nt'):
        return True
    
    return False

__iswindows__ = iswindows()

def ismacosx():
    if os.name.startswith('posix') and sys.platform.startswith('darwin'):
        return True
    
    return False

__ismacosx__ = ismacosx()

def islinux():
    if os.name.startswith('posix') and sys.platform.startswith('linux'):
        return True
    
    return False

__islinux__ = islinux()
def checkProcessAndKill(process_name):
    try:
        if __iswindows__:
            processList = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE)
        elif __ismacosx__:
            processList = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        else:
            print "can not kill process in unknown OS"
        out, err = processList.communicate()
        for line in out.splitlines():
            if process_name in line:
                if __ismacosx__:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
                elif __iswindows__:
                    pid = int(line.split(None)[1])
                    os.kill(pid, signal.SIGTERM)
                
    except Exception,e:
        print e
def checkProcessAndKillOnwin(serviceType):
    try:
        if __iswindows__ :
            toKillProccessList = ["IEDriverServer.exe","chromedriver.exe"]
            resultlist = []
            if serviceType.lower() == "mc" or serviceType.lower() == "ec" or serviceType.lower() == "tc" :
                toKillProccessList.append("atmgr.exe")
            elif serviceType.lower() == "sc":
                toKillProccessList.append("atscmgr.exe")
                toKillProccessList.append("OUTLOOK.EXE")
            for processName in toKillProccessList:
                p=subprocess.Popen(("taskkill /f /im " + processName),shell=True)
                ret = p.wait()
                print "process name %s ,result %s" %(processName,ret)
                resultlist.append(ret)
            for resultT in resultlist:
                if resultT not in [0]:
                    return False,'stop meeting fail'
            return True,''
                
    except Exception,e:
        print e
        
# checkProcessAndKill('atmgr.exe')
print checkProcessAndKillOnwin("mc")