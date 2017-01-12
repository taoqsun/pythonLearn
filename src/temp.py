# -*- coding: utf-8 -*-
'''
Created on Oct 29, 2015

@author: Administrator
'''
from shutil import copyfile
import os
import subprocess
import time
import urllib
from array import array
import datetime,time
import types
from lib2to3.fixer_util import String
import random
import urllib2
import json
import math
import re

def cprint(log):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " -- " + str(log)
def clearWebexPackage():
        """clear webex package
        @param filePath: service path on windows
        @type filePath: string
        @return: operation result
        @rtype: boolean
        """
        resultlist=[]
        print 'delete Local\Webex directory:'
        p1=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Local\Webex',shell=True)
        ret1 = p1.wait()
        print ret1
        p1.kill()
        resultlist.append(ret1)
        
        print 'delete LocalLow\Webex directory:'
        p2=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\LocalLow\Webex',shell=True) 
        ret2 = p2.wait()
        print ret2
        p2.kill()
        resultlist.append(ret2)
       
        print 'delete ProgramData\Webex directory:'
        p3=subprocess.Popen('rd /s /q C:\ProgramData\Webex',shell=True)
        ret3 = p3.wait()
        print ret3
        p3.kill()
        resultlist.append(ret3)
        
        print 'delete Downloaded Program Files\ieatgpc.dll file:'
        p4=subprocess.Popen('del /f /s /q /a \"C:\Windows\Downloaded Program Files\ieatgpc.dll"',shell=True)
        ret4 = p4.wait()
        print ret4
        p4.kill()
        resultlist.append(ret4)
        
        print 'delete Mozilla\plugins\npatgpc.dll file:'
        p5=subprocess.Popen('del /f /s /q /a C:\Users\Administrator\AppData\Roaming\Mozilla\plugins\npatgpc.dll',shell=True)
        ret5 = p5.wait()
        print ret5
        p5.kill()
        resultlist.append(ret5)
        
        print 'delete Application\Plugins\npatgpc.dll file:'
        p6=subprocess.Popen('del /f /s /q /a C:\Program Files\Google\Chrome\Application\Plugins\npatgpc.dll',shell=True)
        ret6 = p6.wait()
        print ret6
        p6.kill()
        resultlist.append(ret6)
        
        print 'delete Mozilla Firefox\browser\plugins\npatgpc.dl file:'
        p7=subprocess.Popen('del /f /s /q /a C:\Program Files\Mozilla Firefox\browser\plugins\npatgpc.dll',shell=True)
        ret7 = p7.wait()
        print ret7
        p7.kill()
        resultlist.append(ret7)
        
        print 'delete Local\WebEx\ChromeNativeHost\ciscowebexstart.exe file:'                    
        p8=subprocess.Popen('del /f /s /q /a C:\Users\Administrator\AppData\Local\WebEx\ChromeNativeHost\ciscowebexstart.exe',shell=True)
        ret8 = p8.wait()
        print ret8
        p8.kill()
        resultlist.append(ret8)
        
        for resultT in resultlist:
            if resultT in [0,1,2]:
                result = True

def repeatFile(filePath=r'C:\ProgramData\Webex\Webex\T31_MC'):
        """replace GPC File and so on
        @param filePath: service path on windows
        @type filePath: string
        @return: operation result
        @rtype: boolean
        """
        fileFatherPath = r'C:\ProgramData\Webex\Webex'
        fileChildPath = filePath
        cashPath = r'C:\Users\Administrator\AppData\LocalLow\WebEx'
        programPath = r'C:\ProgramData\WebEx'
        downloadPath = r'C:\Windows\Downloaded Program Files'
        pluginPath = r'C:\Users\Administrator\AppData\Roaming\Mozilla\plugins'
        mountFilePath = r'\\10.224.84.5\ta.vscmta.ta\ComponentFile_Pipeline\webex-windows-plugin\release'
        
        filePathList=[programPath,cashPath,downloadPath,pluginPath,fileFatherPath,fileChildPath]
        for fileTemp in filePathList:
#             print 'fileTemp==',fileTemp
            if not os.path.exists(fileTemp):
                try:
#                     print "make dir ",fileTemp
                    os.mkdir(fileTemp)
                    time.sleep(2)
                except Exception,e:
                    print e
                    return False
                           
        mountfileList = []
        for (dirpath, dirnames, filenames) in os.walk(mountFilePath):
            mountfileList.extend(filenames)
            break
        fileT=''
        for fileT in mountfileList:
            if fileT in ['atgpcext.dll','atinst.exe','CiscoWebExUpdate.exe','ieatgpc.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,fileChildPath+'\\'+fileT)
                except Exception,e:
                    print e
                    return False
                    
            if fileT in ['npatgpc.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,pluginPath+'\\'+fileT)
                except Exception,e:
                    print e
                    return False
            if fileT in ['ieatgpc1.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,downloadPath+'\ieatgpc.dll')
                    copyfile(mountFilePath+'\\'+fileT,cashPath+'\ieatgpc.dll')
                    copyfile(mountFilePath+'\\'+fileT,programPath+'\ieatgpc.dll')
                except Exception,e:
                    print e
                    return False
        return True
def createIni(filePath='C:\ProgramData\Webex\Webex\T31_MC'):
        fileList = []
        for (dirpath, dirnames, filenames) in os.walk(filePath):
            fileList.extend(filenames)
            break
        file_handle=None
        fileName=filePath+'\\'+'gpcconfig.ini'
        try:         
            file_handle = open(fileName,"w")
            file_handle.writelines("[disable_download]"+"\n")
            for file in fileList:
                file_handle.writelines(file + "\n")
        except:
            pass
        finally:
            file_handle.close()
def killProcess():
    resultlist = []
#     if self.serviceType.lower() == "mc" or self.serviceType.lower() == "ec" or self.serviceType.lower() == "tc" :
    p1=subprocess.Popen("taskkill /f /im atmgr.exe",shell=True)
    ret1 = p1.wait()
    resultlist.append(ret1)
    for resultT in resultlist:
        print 'resultT===',resultT
        if resultT in [0]:
            return True
#     elif self.serviceType.lower() == "sc":
#         p2=subprocess.Popen("taskkill /f /im atscmgr.exe",shell=True)
#         ret2 = p2.wait()
#         resultlist.append(ret2)
#         for resultT in resultlist:
#             if resultT in [0]:
#                 return True
#     p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
#     out, err = p.communicate()
#     
#     if self.serviceType.lower() == "mc":
#         processName = "Meeting Center"
#     elif self.serviceType.lower() == "ec":
#         processName = "Event Center"
#     elif self.serviceType.lower() == "tc":
#         processName = "Training Center"
#     elif self.serviceType.lower() == "sc":
#         processName = "Session Center"
#     for line in out.splitlines():
# #                     print line
#         if processName in line:
#             pid = int(line.split(None, 1)[0])
#             os.kill(pid, signal.SIGKILL)
#     ret2=p.wait()
#     print ret2
    return False
def downloadAndInstall(downloaddUrl='',isInstall=True):
    downloaddUrl="http://t1wdta03.qa.webex.com/client/T31L/Cisco_WebEx_Add-On.exe11"
    downloadStatus=True
#     if isWindows():
#     savePath="C:\\Cisco_WebEx_Add-On.exe"
#     try:
#         urllib.urlretrieve(downloaddUrl,savePath)
#     except IOError,e:
#         downloadStatus=False
#     if isMacOSX():
#         pass
    
#     if downloadStatus:
#         if isInstall:
#             if isWindows():
#     ret1=''
#     try:
#         p1=subprocess.Popen("C:\\Cisco_WebEx_Add-On.exe")
#         ret1=p1.wait()
#     except Exception,e:
#         print 'eee=',e
#     print 'dddd=',ret1
#             if isMacOSX():
#                 pass
#             
#     print "lll===",downloadStatus
    print 'path===',os.path.dirname(__file__)
    print 'path2===',os.path.split(os.path.dirname(__file__))[0]
    print 'path3===',os.path.dirname(os.path.realpath(__file__))
    return downloadStatus
#  clearWebexPackage()

# print type(str(datetime.datetime.now())) 
# print 300 / 600
# print 0 / 600
# print 300 % 600 
# print 700 / 600
# print 600 / 600
# print 700 % 600  

# howToRun(91)
from datetime import datetime
data_object = datetime.strptime('19:34:00', '%H:%M:%S')
data_object2 = datetime.strptime('19:35:00', '%H:%M:%S')
# print (data_object - data_object2).seconds
win_at_Least = random.randint(0,10)
mac_at_Least = random.randint(0,10)
# print   win_at_Least,mac_at_Least 

tempList = [2,3]
# print tempList
# del tempList[:]
# print tempList

# print testCC()
# print range(3)
class urllibRequest(urllib2.Request):
    def __init__(self,method,*args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self,*args,**kwargs)

    def get_method(self):
        return self._method
# __requestURL = "http://taconsole.qa.webex.com/taconsole/service/machine/"
# req = urllibRequest('GET',url=__requestURL + '%s' % ("10.225.23.55"))
# 
# u = urllib2.urlopen(req)
# creationResp = json.loads(u.read())
# print creationResp
# u.close() 
# print ' ceil 1 =>',math.ceil(2.3)
# print math.ceil(2.6) 
# print math.ceil(2)
# print int(math.ceil(2.6))
# from collections import namedtuple
# 
# RequiredMachineCount = namedtuple('RequiredMachineCount', ['win_at_least','win_at_best','mac_at_least','mac_at_best'], rename = True)
# print type(RequiredMachineCount)
# print isinstance(RequiredMachineCount,type)
# dictTemp = {"1":"a","2":"b","3":4}
# for c,d in dictTemp.iteritems():
#     print c,d
def howToWait(totalWaitTime,sizeList = [600,60,5,1]):
    loopList = []
    for indexTemp in range(len(sizeList)):
        loopTimes = totalWaitTime / sizeList[indexTemp]
        if loopTimes != 0:
            loopList.append(loopTimes)
            totalWaitTime = totalWaitTime - (loopTimes * sizeList[indexTemp]) 
            continue
        else:
            loopList.append(0)
    cprint( str(loopList) )
    for indexLoopList in range(len(loopList)):
        indexT = 0
        if loopList[indexLoopList] == 0:
            continue
        for indexT in range(loopList[indexLoopList]):
            cprint("the " + str(indexT+1)+" times , to wait time :" + str(sizeList[indexLoopList]) + "s ...... " )
            time.sleep(sizeList[indexLoopList])
# howToWait(10)
# cprint(str(range(2)) )   
# print math.ceil(0)  
# print str(None)
# print re.search(r'.git', "stringit")
# _howToWait(30)
# repeatFile()
# createIni()
# killProcess()
# downloadAndInstall()
# 
# fileName=[]
# if getOSName() != '':
#     fileName.append(getOSName())
# if args.serviceName != None:
#     fileName.append(args.serviceName)
# if args.browserName != None:
#     fileName.append(args.browserName)
# if args.downloadType != None:
#     fileName.append(args.downloadType)
# report_file = fileTemp + os.sep +'_'.join(fileName)+'.xml'

# import os
# 
# def getpid(s):
# 
#     im='"IMAGENAME eq %s"'%s
#     cmd="tasklist /NH /FI %s"%im
#     cmd = '''for /f \"tokens=2 delims=,"'''+''' %F'''+" in ('tasklist /nh /fi %s"%im+" /fo csv') do @echo %~F"
# #     for /f "tokens=2 delims=," %F in ('tasklist /nh /fi "imagename eq BitTorrent.exe" /fo csv') do @echo %~F
#     s=os.popen(cmd).read()
#     print s
#     list11=s.split("\n")
#     print list11
#     print filter(None, list11)
#     print len(s)
#     print s[0:5]
# 
# print getpid('iexple.exe')
# windowsList=[0,1,2,3,4,5]
# getBrowserPID=["1","2",""]
# windowsList2=[]
# tryTimes = 0
# installButtonList = []
# oBrowser=[1,3,5]
# c=0
# for window1 in windowsList:
#     for pid1 in getBrowserPID:
#         print "888===",window1
#         print "999===",pid1
#         if window1 == pid1:
#             oBrowser = window1
#             break
#         c=c+1
#         print c
# print filter(None, getBrowserPID)
# print [x+x for x in windowsList if x%2 == 0]
# print [windowsList[x] for x in range(len(windowsList))]
# for a,b in zip(windowsList,getBrowserPID):
#     print (str(a)+b)

# while len(installButtonList) == 0 and tryTimes <= 30:
#     for pyWinBrowser in oBrowser:
#         if pyWinBrowser % 2 == 0:
#             installButtonList.append(pyWinBrowser)
#         if 0 != len(installButtonList):
#             break
#     time.sleep(1)
#     tryTimes = tryTimes + 1
# print installButtonList
# sorted(dictTemp.iteritems(),key=lambda dictTemp:dictTemp[1]["start_time"],reverse= False)

listTemp = [['1',1],['2',2],['0',0]]
print sorted(listTemp,key=lambda x:x[1],reverse= False)
c = 1
if c >=0 and c<=10:
    print "dd"
    
launchCache  = [1,2,3]
print "the scripts will to trigger : " + "\n".join(str(v) for v in launchCache)
print launchCache
for keyTemp in launchCache:
    print "before == ",launchCache
    launchCache.remove(keyTemp)
    print "after == ",launchCache
    print keyTemp
#     print launchCache.index(keyTemp)
    
    
print "none = ",str(None)   
tempFF = [None,333,"tt"]
print "qq =" , filter(None, tempFF)
strCurTime = "16:34:05"
startTimeValue = "16:34:00"
print (datetime.strptime(startTimeValue,"%H:%M:%S") - datetime.strptime(strCurTime,"%H:%M:%S")).seconds

if datetime.strptime(startTimeValue,"%H:%M:%S") < datetime.strptime(strCurTime,"%H:%M:%S"):
    print "22"

print os.path.join("c:","ggg","ff")
listRR = [1,2,3]
print listRR[-1]


globvar = 0
print "before is ",globvar
def set_globvar_to_one():
    global globvar    # Needed to modify global copy of globvar
    globvar = 1

def print_globvar():
    print "print_globvar() is ",globvar     # No need for global declaration to read value of globvar

set_globvar_to_one()
print_globvar()       # Prints 1

print os.path.basename(os.getenv("appdata"))
print os.path.dirname(os.getenv("appdata"))
# timeDef = (datetime.strptime(startTimeValue,"%H:%M:%S") - datetime.strptime(strCurTime,"%H:%M:%S")).seconds - 86400
# print "==== ",timeDef 