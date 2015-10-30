# -*- coding: utf-8 -*-
'''
Created on Oct 29, 2015

@author: Administrator
'''
from shutil import copyfile
import os
import subprocess
import time

def clearWebexPackage():
        """clear webex package
        @param filePath: service path on windows
        @type filePath: string
        @return: operation result
        @rtype: boolean
        """
        result=False
#         if isWindows():
        resultlist=[]
        p1=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Local\Webex',shell=True)
        ret1 = p1.wait()
        resultlist.append(ret1)
        p2=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\LocalLow\Webex',shell=True) 
        ret2 = p2.wait()
        resultlist.append(ret2)
        p3=subprocess.Popen('rd /s /q C:\ProgramData\Webex',shell=True)
        ret3 = p3.wait()
        resultlist.append(ret3)
        p4=subprocess.Popen('rd /s /q \"C:\Windows\Downloaded Program Files\"',shell=True)
        ret4 = p4.wait()
        resultlist.append(ret4)
        p5=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Roaming\Mozilla\plugins',shell=True)
        ret5 = p5.wait()
        resultlist.append(ret5)
        for resultT in resultlist:
            if resultT in [0,2]:
                result = True
            else:
                result = False
#         elif isMacOSX():
#             resultlist=[]   
#             p6=subprocess.Popen('rm -rf ~/Library/Application\ Support/WebEx\ Folder',shell=True) 
#             ret6 = p6.wait()
#             resultlist.append(ret6)
#             for resultT in resultlist:
#                 if resultT in [0]:
#                     result = True
#                 else:
#                     result = False
        print "clear result==",result
        return result

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
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    if self.serviceType.lower() == "mc":
        processName = "Meeting Center"
    elif self.serviceType.lower() == "ec":
        processName = "Event Center"
    elif self.serviceType.lower() == "tc":
        processName = "Training Center"
    elif self.serviceType.lower() == "sc":
        processName = "Session Center"
    for line in out.splitlines():
#                     print line
        if processName in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
    ret2=p.wait()
    print ret2
    return False
# clearWebexPackage()
# repeatFile()
# createIni()
# killProcess()