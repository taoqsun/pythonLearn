'''
Created on Feb 17, 2016

@author: sky
'''
import os
from shutil import copyfile
import subprocess

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
                     
#         elif isMacOSX():
#             resultlist=[]   
#             p6=subprocess.Popen('rm -rf ~/Library/Application\ Support/WebEx\ Folder',shell=True) 
#             ret6 = p6.wait()
#             resultlist.append(ret6)
#             for resultT in resultlist:
#                 if resultT in [0]:
#                     result = True
        return result
    
def clearWebexPackage1():
        """clear webex package
        @param filePath: service path on windows
        @type filePath: string
        @return: operation result
        @rtype: boolean
        """
        result=False
#         if isWindows():

        resultlist=[]
        directoryList = ['C:\Users\Administrator\AppData\Local\Webex','C:\Users\Administrator\AppData\LocalLow\Webex',
                         'C:\ProgramData\Webex']
        for dire in directoryList:
            print 'delete directory :' + dire
            p = subprocess.Popen(('rd /s /q '+dire),shell = True)
            ret = p.wait()
            print 'delete directory result :' + str(ret)
            p.kill()
            resultlist.append(ret)

        filePathList = [r'C:\Windows\Downloaded Program Files\ieatgpc.dll',
                        r'C:\Users\Administrator\AppData\Roaming\Mozilla\plugins\npatgpc.dll',
                         r'C:\Program Files\Google\Chrome\Application\Plugins\npatgpc.dll',
                         r'C:\Program Files\Mozilla Firefox\browser\plugins\npatgpc.dll',
                         r'C:\Users\Administrator\AppData\Local\WebEx\ChromeNativeHost\ciscowebexstart.exe']
        for file in filePathList:
            print 'delete file :' + file
            p = subprocess.Popen(('del /f /s /q /a '+'"'+file+'"'),shell = True)
            ret = p.wait()
            print 'delete file result :' + str(ret)
            p.kill()
            resultlist.append(ret)

        
        for resultT in resultlist:
            if resultT in [0,1,2]:
                result = True
                     
#         elif isMacOSX():
#             resultlist=[]   
#             p6=subprocess.Popen('rm -rf ~/Library/Application\ Support/WebEx\ Folder',shell=True) 
#             ret6 = p6.wait()
#             resultlist.append(ret6)
#             for resultT in resultlist:
#                 if resultT in [0]:
#                     result = True
        return result
def createIni(filePath=''):
        """create INI config File 
        @param filePath: service path on windows
        @type filePath: string
        @return: operation result
        @rtype: boolean
        """
        print "start creat INI file...."
        fileList = []
#         for (dirpath, dirnames, filenames) in os.walk(filePath):
#             fileList.extend(filenames)
#             break
        if filePath.endswith('C'):
            fileList = ['atgpcext.dll','atinst.exe']
        
        if filePath.endswith('ins'):
            fileList = ['npatgpc.dll']    
            
        file_handle=None
        fileName=filePath+'\\'+'gpcconfig.ini'
        try:         
            file_handle = open(fileName,"w")
            file_handle.writelines("[disable_download]"+"\n")
            numTemp = 1
            for fileT in fileList:
                file_handle.writelines('file'+str(numTemp)+'='+fileT + "\n")
                numTemp = numTemp+1
        except:
            return False
        finally:
            file_handle.close()
        return True
    
def replaceFile(filePath='',IsChrome = False):
#         if isWindows():
        print "start replace some DLL file......"
        fileFatherPath = r'C:\ProgramData\Webex\Webex'
        fileChildPath = filePath
        cashPath = r'C:\Users\Administrator\AppData\LocalLow\WebEx'
        programPath = r'C:\ProgramData\WebEx'
        downloadPath = r'C:\Windows\Downloaded Program Files'
        pluginPath = r'C:\Users\Administrator\AppData\Roaming\Mozilla\plugins'
        pluginPath1 = r'C:\Program Files\Google\Chrome\Application\Plugins'
        pluginPath2 = r'C:\Program Files\Mozilla Firefox\browser\plugins'
        ChromeAddOnPath = r'C:\Users\Administrator\AppData\Local\WebEx'
        ChromeAddOnPath2 = r'C:\Users\Administrator\AppData\Local\WebEx\ChromeNativeHost'
        mountFilePath = r'\\10.224.84.5\ta.vscmta.ta\ComponentFile_Pipeline\webex-windows-plugin\release'
        mountFilePathForChromeAddOn = r'\\10.224.84.5\ta.vscmta.ta\ComponentFile_Pipeline\webex-chrome-addon\release'
         
        filePathList=[programPath,cashPath,downloadPath,pluginPath,
                  fileFatherPath,fileChildPath,pluginPath1,pluginPath2,ChromeAddOnPath,ChromeAddOnPath2]
        for fileTemp in filePathList:
#             print 'fileTemp==',fileTemp
            if not os.path.exists(fileTemp):
                try:
                    os.mkdir(fileTemp)
                except Exception,e:
                    print e
        
        downloadfDirList = []
        for (dirpath, dirnames, filenames) in os.walk(downloadPath):
            downloadfDirList.extend(dirnames)
            break
        DirT=''
        for DirT in downloadfDirList:
            print "directory ====>",downloadPath + os.sep + DirT
            try:
                if os.path.isfile(downloadPath + os.sep + DirT +'\ieatgpc.dll'):
                    print "remove ",downloadPath + os.sep + DirT +'\ieatgpc.dll'
                    os.remove(downloadPath + os.sep + DirT +'\ieatgpc.dll')
#                     p8=subprocess.Popen(('del /f /s /q /a '+ downloadPath + os.sep + DirT +'\ieatgpc.dll'),shell=True)
#                     ret8 = p8.wait()
#                     print "55555555555===>",ret8
#                     p8.kill()
                copyfile(mountFilePath+'\\'+'ieatgpc1.dll',downloadPath + os.sep + DirT +'\ieatgpc.dll')
            except Exception,e:
                print e
                            
        mountfileList = []
        for (dirpath, dirnames, filenames) in os.walk(mountFilePath):
            mountfileList.extend(filenames)
            break
        fileT=''
        for fileT in mountfileList:
            if fileT in ['atgpcext.dll','atinst.exe']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,fileChildPath+'\\'+fileT)
                except Exception,e:
                    print e

                     
            if fileT in ['npatgpc.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,pluginPath+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath1+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath2+'\\'+fileT)
                except Exception,e:
                    print e

            if fileT in ['ieatgpc1.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,downloadPath+'\ieatgpc.dll')
                    copyfile(mountFilePath+'\\'+fileT,cashPath+'\ieatgpc.dll')
                    copyfile(mountFilePath+'\\'+fileT,programPath+'\ieatgpc.dll')
                except Exception,e:
                    print e

        if IsChrome:
#             print "replace chrome add on file"
            if not os.path.exists(ChromeAddOnPath):
                try:
                    os.mkdir(ChromeAddOnPath)
                except Exception,e:
                    print e

            try:
                copyfile(mountFilePathForChromeAddOn +'\\CiscoWebExStart.exe', ChromeAddOnPath2+'\\ciscowebexstart.exe')
            except Exception,e:
                print e

         
        return True

clearWebexPackage1()
# 
replaceFile(r'C:\ProgramData\Webex\Webex\T31_TC')
createIni(r'C:\ProgramData\Webex\Webex\T31_TC')