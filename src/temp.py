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
#         resultlist=[]
        
#         if isWindows():
#         p1=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Local\Webex',shell=True)
#         ret1 = p1.wait()
#         resultlist.append(ret1)
#         p2=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\LocalLow\Webex',shell=True) 
#         ret2 = p2.wait()
#         resultlist.append(ret2)
#         p3=subprocess.Popen('rd /s /q C:\ProgramData\Webex',shell=True)
#         ret3 = p3.wait()
#         resultlist.append(ret3)
#         p4=subprocess.Popen('rd /s /q \"C:\Windows\Downloaded Program Files\"',shell=True)
#         ret4 = p4.wait()
#         resultlist.append(ret4)
#         p5=subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Roaming\Mozilla\plugins',shell=True)
#         ret5 = p5.wait()
#         resultlist.append(ret5)
#         for result in resultlist:
#             if result in [0,2]:
#                 return True
#             else:
#                 return False
        
        resultlist=[]   
        p6=subprocess.Popen('rm -rf ~/Library/Application\ Support/WebEx\ Folder',shell=True) 
        ret6 = p6.wait()
        for resultT in resultlist:
            print resultT
            if resultT in [0,2]:
                result = True
            else:
                result = False
        print result
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
clearWebexPackage()
# repeatFile()
# createIni()