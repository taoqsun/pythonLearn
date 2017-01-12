'''
Created on Feb 17, 2016

@author: sky
'''
import os
from shutil import copyfile
import subprocess

#set global variable for mount point
mountPoint = r'\\10.194.246.26\vol_ta_data\spare\share\clientta' #for American environment
#mountPoint = r'\\10.224.84.31\engta'#for hefei environment
appDataPath = os.path.dirname(os.getenv("appdata"))

def clearWebexPackage():
    """clear webex package
    @param filePath: service path on windows
    @type filePath: string
    @return: operation result 
    @rtype: tuple
    """
    result = False,'clear package fail'
    if 0 == 0:
        resultlist=[]
        resultlist=[]
        directoryList = [os.path.join(appDataPath,'Local\Webex'),
                         os.path.join(appDataPath,'LocalLow\Webex'),
                         'C:\ProgramData\Webex']
        for dire in directoryList:
            print 'delete directory :' + dire
            p = subprocess.Popen(('rd /s /q '+dire),shell = True)
            ret = p.wait()
            print 'delete directory result :' + str(ret)
            p.kill()
            resultlist.append(ret)

        filePathList = [r'C:\Windows\Downloaded Program Files\ieatgpc.dll',
                        os.path.join(appDataPath,'Roaming\Mozilla\plugins\npatgpc.dll'),
                         r'C:\Program Files\Google\Chrome\Application\Plugins\npatgpc.dll',
                         r'C:\Program Files (x86)\Google\Chrome\Application\Plugins\npatgpc.dll',
                         r'C:\Program Files\Mozilla Firefox\browser\plugins\npatgpc.dll',
                         r'C:\Program Files (x86)\Mozilla Firefox\browser\plugins\npatgpc.dll',
                         os.path.join(appDataPath,'Local\WebEx\NativeMessagingHosts\ciscowebexstart.exe')]
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
                
            
    elif 0 != 0:
#         ~/Library/Application Support/WebEx Folder
#         ~/Library/Internet Plug-Ins/WebEx64.plugin
#         ~/Library/Application Support/Mozilla/NativeMessagingHosts/com.webex.meeting.json
#         ~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.webex.meeting.json
#         ~/Library/Application Support/Google/Chrome Canary/NativeMessagingHosts/com.webex.meeting.json
        
        resultlist = []
        toDelList = ['~/Library/Application\ Support/WebEx\ Folder',
                     '~/Library/Internet\ Plug-Ins/WebEx64.plugin',
                     '~/Library/Application\ Support/Mozilla/NativeMessagingHosts/com.webex.meeting.json',
                     '~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.webex.meeting.json',
                     '~/Library/Application\ Support/Google/Chrome\ Canary/NativeMessagingHosts/com.webex.meeting.json']   
        for toDelItem in toDelList:
            p = subprocess.Popen(('rm -Rf ' + toDelItem),shell=True) 
            ret = p.wait()
            resultlist.append(ret)
            for resultT in resultlist:
                if resultT in [0]:
                    result = True,''
    return result

def copyCoverageFile():
#     covFileSourcePath = r'\\tanfs.eng.webex.com\engta\share\clientta\ComponentFile_Pipeline\webex-windows-plugin\test.cov'
    covFileSourcePath = mountPoint + r'\ComponentFile_Pipeline\webex-windows-plugin\test.cov'
    jobPath = r'C:\client_mb_job\test.cov'
    try:
        copyfile(covFileSourcePath,jobPath)
    except Exception,e:
        print e

def upLoadCoverageFile(BuildlVer,BuildNum):
#     //tanfs.eng.webex.com/engta/share/clientta/curl.exe
    uploadCOVFileCommand = mountPoint + r"\curl.exe -F " + '"' + "file=@C:\client_mb_job\\test.cov;filename=test.cov" + '"' + " " + '"' + \
                            "http://tacoveragews.qa.webex.com/webex-coverage-ws/testdata.do?action=upload&datatype=rawdata&componentname=webex-windows-plugin&"+ \
                            "buildver=" + BuildlVer + "&buildnum="+ BuildNum + '"'
    p = subprocess.Popen((uploadCOVFileCommand),shell = True)
    ret = p.wait()
    p.kill()

     
def replaceFile(filePath,strVersion,IsChrome = False):
    """replace GPC File and so on
    @param filePath: service path on windows
    @type filePath: string
    @type IsChrome: boolean
    @return: operation result
    @rtype: boolean
    """
    if 0 == 0:
        print "start replace some DLL file......"
        fileFatherPath = r'C:\ProgramData\Webex\Webex'
        fileChildPath = filePath
        
        cashPath = os.path.join(appDataPath , 'LocalLow\WebEx')
        programPath = r'C:\ProgramData\WebEx'
        downloadPath = r'C:\Windows\Downloaded Program Files'
        
        pluginPath = os.path.join(appDataPath , 'Roaming\Mozilla\plugins')
        pluginPath1 = r'C:\Program Files\Google\Chrome\Application\Plugins'
        pluginPath2 = r'C:\Program Files (x86)\Google\Chrome\Application\Plugins'
        pluginPath3 = r'C:\Program Files\Mozilla Firefox\browser\plugins'
        pluginPath4 = r'C:\Program Files (x86)\Mozilla Firefox\browser\plugins'
        
        ChromeAddOnPath = os.path.join(appDataPath , 'Local\WebEx')
        ChromeAddOnPath2 = os.path.join(appDataPath , 'Local\WebEx\NativeMessagingHosts')
        
        
        mountFilePath = mountPoint + r'\ComponentFile_Pipeline\webex-windows-plugin.' + strVersion + r'\release'
        mountFilePathForChromeAddOn = mountPoint + r'\ComponentFile_Pipeline\webex-chrome-addon.' + strVersion + r'\release'
        
        
        print "mountFilePath = %s , mountFilePathForChromeAddOn = %s" % (mountFilePath,mountFilePathForChromeAddOn)
         
        filePathList=[programPath,cashPath,downloadPath,pluginPath,
                  fileFatherPath,fileChildPath,pluginPath1,pluginPath2,
                  ChromeAddOnPath,ChromeAddOnPath2]
        
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
                    if not os.path.exists(pluginPath):
                        os.makedirs(pluginPath)
                    if not os.path.exists(pluginPath1):
                        os.makedirs(pluginPath1)
                    if not os.path.exists(pluginPath2):
                        os.makedirs(pluginPath2)
                    if not os.path.exists(pluginPath3):
                        os.makedirs(pluginPath3)
                    if not os.path.exists(pluginPath4):
                        os.makedirs(pluginPath4)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath1+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath2+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath3+'\\'+fileT)
                    copyfile(mountFilePath+'\\'+fileT,pluginPath4+'\\'+fileT)
                except Exception,e:
                    print e

            if fileT in ['ieatgpc1.dll']:
                try:
                    copyfile(mountFilePath+'\\'+fileT,downloadPath+'\ieatgpc.dll')
                    os.system(os.path.split(os.path.dirname(__file__))[0]+'\\tool\\Registgpc.bat')
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
                copyfile(mountFilePathForChromeAddOn +'\\CiscoWebExStart.exe', 
                         ChromeAddOnPath2+'\\ciscowebexstart.exe')
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

replaceFile(r'C:\ProgramData\Webex\Webex\T31_UMC',"31.10.0.1832")
createIni(r'C:\ProgramData\Webex\Webex\T31_UMC')
createIni(r'C:\Users\Administrator\AppData\Roaming\Mozilla\plugins')
