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
    @rtype: tuple
    """
    result = False,'clear package fail'
    
    resultlist=[]
    resultlist=[]
    directoryList = ['C:\Users\Administrator\AppData\Local\Webex',
                     'C:\Users\Administrator\AppData\LocalLow\Webex',
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
            result = True,''
                
            
    
    return result
     
def replaceFile(filePath='',IsChrome = False):
    
    
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

clearWebexPackage()

replaceFile(r'C:\ProgramData\Webex\Webex\T31_TC')
createIni(r'C:\ProgramData\Webex\Webex\T31_TC')