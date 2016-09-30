""" PreMeeting class and related functions definition
@author: taoqsun
@date: 2015-09-09
@see: N/A
"""

import time
import os
from common.PyLog import PyLog as logs
from meeting.BrowserFactory import BrowserFactory
from common.PyConsts import PyLanguageId, PyLocaleId
from meeting.MeetingConstants import MeetingConstants
from subprocess import Popen
from shutil import copyfile
try:
    from common import isWindows,isMacOSX,ThreeItemsOperator
except ImportError:
    pass
import urllib
import subprocess, signal
from cfw.mainFrame import *
from sessiondata.jmt import JMTData

def clearWebexPackage():
    """clear webex package
    @param filePath: service path on windows
    @type filePath: string
    @return: operation result 
    @rtype: tuple
    """
    result = False,'clear package fail'
    if isWindows():
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
                         r'C:\Program Files (x86)\Google\Chrome\Application\Plugins\npatgpc.dll',
                         r'C:\Program Files\Mozilla Firefox\browser\plugins\npatgpc.dll',
                         r'C:\Program Files (x86)\Mozilla Firefox\browser\plugins\npatgpc.dll',
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
                
            
    elif isMacOSX():
        resultlist=[]   
        p6=subprocess.Popen('rm -rf ~/Library/Application\ Support/WebEx\ Folder',shell=True) 
        ret6 = p6.wait()
        resultlist.append(ret6)
        for resultT in resultlist:
            if resultT in [0]:
                result = True,''
    return result

def copyCoverageFile():
    print "begin to copy \\10.224.84.31\engta\ComponentFile_Pipeline\webex-windows-plugin\test.cov ..... "
    covFileSourcePath = r'\\10.224.84.31\engta\ComponentFile_Pipeline\webex-windows-plugin\test.cov'
    jobPath = r'C:\client_mb_job\test.cov'
    try:
        copyfile(covFileSourcePath,jobPath)
    except Exception,e:
        print e

def upLoadCoverageFile(BuildlVer,BuildNum):
    
    uploadCOVFileCommand = "\\\\10.224.84.31\engta\curl.exe -F " + '"' + "file=@C:\client_mb_job\\test.cov;filename=test.cov" + '"' + " " + '"' + \
                            "http://tacoveragews.qa.webex.com/webex-coverage-ws/testdata.do?action=upload&datatype=rawdata&componentname=webex-windows-plugin&"+ \
                            "buildver=" + BuildlVer + "&buildnum="+ BuildNum + '"'
    print 'upload COV file command = :' + uploadCOVFileCommand
    p = subprocess.Popen((uploadCOVFileCommand),shell = True)
    ret = p.wait()
    print 'upload COV file result : ' + str(ret)
    p.kill()

     
def replaceFile(filePath='',IsChrome = False):
    """replace GPC File and so on
    @param filePath: service path on windows
    @type filePath: string
    @param IsChrome: whether to copy chrome addon file，default is copy this file.
    @type IsChrome: boolean
    @return: operation result
    @rtype: boolean
    """
    if isWindows():
        print "start replace some DLL file......"
        fileFatherPath = r'C:\ProgramData\Webex\Webex'
        fileChildPath = filePath
        cashPath = r'C:\Users\Administrator\AppData\LocalLow\WebEx'
        programPath = r'C:\ProgramData\WebEx'
        downloadPath = r'C:\Windows\Downloaded Program Files'
        pluginPath = r'C:\Users\Administrator\AppData\Roaming\Mozilla\plugins'
        pluginPath1 = r'C:\Program Files\Google\Chrome\Application\Plugins'
        pluginPath2 = r'C:\Program Files (x86)\Google\Chrome\Application\Plugins'
        pluginPath3 = r'C:\Program Files\Mozilla Firefox\browser\plugins'
        pluginPath4 = r'C:\Program Files (x86)\Mozilla Firefox\browser\plugins'
        ChromeAddOnPath = r'C:\Users\Administrator\AppData\Local\WebEx'
        ChromeAddOnPath2 = r'C:\Users\Administrator\AppData\Local\WebEx\ChromeNativeHost'
        mountFilePath = r'\\tanfs.eng.webex.com\engta\share\clientta\ComponentFile_Pipeline\webex-windows-plugin\release'
        mountFilePathForChromeAddOn = r'\\tanfs.eng.webex.com\engta\share\clientta\ComponentFile_Pipeline\webex-chrome-addon\release'
        
         
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

class wbxMeeting(object):
    """Handle schedule, start, join meeting according siteUrl, languageId account etc.
    """
    def __init__(self, site_Domain,site_Name,browserName,serviceType,
                 acount,meetingPassword,teleInfo,meetingTopic,downloadType):
        if site_Name != '':
            self.siteUrl = site_Domain + '/' + site_Name
        else:
            self.siteUrl = site_Domain
        self.browserName=browserName
        self.log = logs()
        self.myDriver = BrowserFactory.getBrowser(self.browserName)
        self.ticket = ''
        self.serviceType = serviceType
        self.acount = acount
        self.meetingPassword = meetingPassword
        self.teleInfo = teleInfo
        self.meetingTopic = meetingTopic
        self._jmtData = JMTData()
        self.downloadType = downloadType
        self.realmeetingTopic = ""
        self.meetingKey = ''
        
    def getJMTData(self):
        return self._jmtData
        
    def setTelephoneConfig(self, teleInfo):
        self.teleInfo = teleInfo
                 
    def isPreMeetingInfoValid(self):
        """Check if meeting information params is valid
        @return: True when all params are valid,otherwise return False
        @rtype: boolean     
        """
        if (self.siteUrl == '' ):
            self.log.fdbg(os.path.normpath(__file__) + '==>isPreMeetingInfoValid : siteUrl = ' + self.siteUrl )
            return False
        
        if (not self.siteUrl.endswith('/')):
            self.siteUrl = self.siteUrl + '/'
        
        if (self.myDriver == None):
            return False
        
        return True
           
    def switchService(self,serviceType):
        """Switch service type such as between MC and TC
        @param serviceType: change to service name
        @type serviceType: string
        @return: True and none string when switch successfully,otherwise return False and error message
        @rtype: tuple     
        """
        e = ''
        self.serviceType = serviceType
        switchSericeResult = True
        if (not self.isPreMeetingInfoValid()):
            self.log.fdbg(os.path.normpath(__file__) + '==>switchService : Previous meeting info is not valid.')
            return False,'switchService : Previous meeting info is not valid'
        url = self.siteUrl + 'o.php?AT=ST&SP=' + serviceType
        self.log.fdbg(os.path.normpath(__file__) + '==>switchService : url = ' + url)
        self.myDriver.get(url)
        afterSwitchSericeReturnResult=self.myDriver.page_source
        afterSwitchServiceUrl = str(self.myDriver.current_url)
        self.log.fdbg(os.path.normpath(__file__) + '==>after SwitchService Url' + afterSwitchServiceUrl)
#         print "afterSwitchSericeUrl====",afterSwitchSericeReturnResult
        try:
            if (str(afterSwitchSericeReturnResult).find("SUCCESS") == -1) :
                switchSericeResult = False
        except Exception,e :
            switchSericeResult = False
#             print e
                
        return switchSericeResult,e
       
    def switchLanguage(self,languageId,localeId,isHost):
        """Switch language to launch localizable meeting.
        @param languageId: change to language ID
        @type languageId: string
        @param localeId: change to location ID
        @type localeId: string
        @param isHost: Whether is Host role, default = True
        @type isHost: boolean
        @return: True and none string when switch successfully,otherwise return False and error message
        @rtype: tuple     
        """
        
        if (not self.isPreMeetingInfoValid()):
            self.log.fdbg(os.path.normpath(__file__) + '==>switchLanguage : Previous meeting info is not valid.')
            return False,'switchLanguage : Previous meeting info is not valid.'
        
        if (isHost):
            action = 'AT=MO'
        else:
            action = 'AT=AP'
        url = self.siteUrl + 'o.php?' + action + '&Language=' + languageId + '&Locale=' + localeId
        self.log.fdbg(os.path.normpath(__file__) + '==>switchLanguage : url = ' + url)
        self.myDriver.get(url)
        switchLanguageCurrenUrl=str(self.myDriver.current_url)
        self.log.fdbg(os.path.normpath(__file__) + '==>after Switch language Url' + switchLanguageCurrenUrl)
        if (switchLanguageCurrenUrl.find("SUCCESS") == -1) :
            self.log.fdbg(os.path.normpath(__file__) + '==>switch Language  fail')
            return False,'switch Language  fail'
            
        return True,''
    
    def loginSite(self,acount):
        """Login an in progress meeting by valid account.
        @param acount: An object which include user name, password, details please refer to Account class
        @type acount: Account object
        @return: True and none string when login site successfully,otherwise return False and error message
        @rtype: tuple     
        """
        self.acount = acount
        loginStatus=True
        e = ''
        if (not self.isPreMeetingInfoValid()):
            self.log.fdbg(os.path.normpath(__file__) + '==>loginSite : Previous meeting info is not valid.')
            return False,'loginSite : Previous meeting info is not valid.'
        
        url = self.siteUrl + 'p.php?AT=' + 'LI' + '&WID=' + self.acount.userName + '&PW=' + self.acount.password
        self.log.fdbg(os.path.normpath(__file__) + '==>loginSite : url = ' + url)
#         print 'loginUrl=',url
        self.myDriver.get(url)
        self.myDriver.maximize_window()
        currentUrl=str(self.myDriver.current_url)
        self.log.fdbg(os.path.normpath(__file__) + '==>after login meeting Url' + currentUrl)
#         print "currentUrl===",currentUrl
        if (currentUrl.find("&ST") != -1):
            statusIndex = currentUrl.find("&ST")
            loginStatus=currentUrl[statusIndex+4:statusIndex+8]
             
        if (loginStatus == "FAIL"):
            self.log.fdbg(os.path.normpath(__file__) + '==>loginSite fail')
            e = 'loginSite fail'
            loginStatus = False
        
        return loginStatus,e
    
    def waitForMeetingStarted(self,i_time_out,isT30 = False):
        if isT30:
            if 0 == waitForMainFrame(i_time_out,self.serviceType,True): #time out
                self._jmtData._end_time = 0
    #             print "the end time ",self.__jmtData._end_time
                return False
            else:
                self._jmtData._end_time = time.time()
    #             print "the end time ",self.__jmtData._end_time
                return True
        else:
            if 0 == waitForMainFrame(i_time_out,self.serviceType): #time out
                self._jmtData._end_time = 0
    #             print "the end time ",self.__jmtData._end_time
                return False
            else:
                self._jmtData._end_time = time.time()
    #             print "the end time ",self.__jmtData._end_time
                return True
        
    def closeBrowser(self):
        """close the browser
        """
        self.myDriver.quit()

    def logoutMeeing(self):
        """Logout a meeting
        @return: True when switch successfully,otherwise return False
        @rtype: boolean     
        """
        if (self.serviceType == MeetingConstants.SupportCenter):
            logoutAction = 'p.php?AT=LS'
        else:
            logoutAction = 'p.php?AT=LO'
            
        url = self.siteUrl + logoutAction
        self.log.fdbg(os.path.normpath(__file__) + '==>logoutMeeing : url = ' + url)
        print 'logoutMeetingUrl=',url
        
        self.myDriver.get(url)

    def scheduleMeeting(self,ramdomNo=""):
        """Schedule a meeting by valid account.
        @param ramdamNo: ramdom number
        @type ramdamNo:string
        @return: true and meeting key when schedule successfully,otherwise return false and error message
        @rtype: tuple
        """
        if (not self.isPreMeetingInfoValid()):
            self.log.fdbg(os.path.normpath(__file__) + '==>scheduleMeeting : Previous meeting info is not valid.')
            return False,'scheduleMeeting : Previous meeting info is not valid.'
        
        loginResult=self.loginSite(self.acount)
#         print "loginResult ===",loginResult
        if (loginResult[0] == False):
            self.log.fdbg(os.path.normpath(__file__) + '==>scheduleMeeting : login meeting false')
            return False,'scheduleMeeting : login meeting false'
        switchSericeResult = self.switchService(self.serviceType)
#         print "switchSericeResult===",switchSericeResult
        if ramdomNo != "":
                self.realmeetingTopic =  self.meetingTopic  + str(ramdomNo)
        else:
                self.realmeetingTopic =  self.meetingTopic
        trackingCodesParam = "&TC1=1&TC2=2&TC3=3&TC4=4&TC5=5&TC6=6&TC7=7&TC8=8&TC9=9&TC10=10"
        if (self.serviceType == MeetingConstants.EventCenter):
            scheduleAction = "SE"
            encodedMtgTopicParam = '&' + urllib.urlencode({'EN':self.realmeetingTopic})
            passwordParam = '&JPW=' + self.meetingPassword
            requireRegistration = '&WIRE=0'
        elif (self.serviceType == MeetingConstants.SupportCenter):
            scheduleAction = "SK"
            encodedMtgTopicParam = ''
            passwordParam = ''
            requireRegistration = ''
        else:
            scheduleAction = "SM"
            encodedMtgTopicParam = '&' + urllib.urlencode({'MN':self.realmeetingTopic})
            passwordParam = '&PW=' + self.meetingPassword
            requireRegistration = ''
            
        scheduleMeetingUrl = self.siteUrl + 'm.php?AT=' + scheduleAction + encodedMtgTopicParam + passwordParam + trackingCodesParam + self.teleInfo.getConfigParam() + \
                                self.teleInfo.getDescriptionParam() + self.teleInfo.gettspAcountParam() + "&LF=1&NT=1" + requireRegistration
        self.log.fdbg(os.path.normpath(__file__) + '==>scheduleMeeting : url = ' + scheduleMeetingUrl)

        if (switchSericeResult[0] != False):
            self.myDriver.get(scheduleMeetingUrl)
            time.sleep(1)
            afterScheduleMeetingReturnResultUrl = str(self.myDriver.current_url)
            self.log.fdbg(os.path.normpath(__file__) + '==>after scheduleMeeting return url = ' + afterScheduleMeetingReturnResultUrl)
            if (afterScheduleMeetingReturnResultUrl.find("&ST") != -1):
                statusIndex=afterScheduleMeetingReturnResultUrl.find("&ST")
                scheduleMeetingStatus=afterScheduleMeetingReturnResultUrl[statusIndex+4:statusIndex+8]
                if scheduleMeetingStatus == "FAIL":
                    self.log.fdbg(os.path.normpath(__file__) + '==>scheduleMeeting fail ')
                    return False,"scheduleMeeting fail"
                else:
                    self.meetingKey = self.parseMeetingKey(afterScheduleMeetingReturnResultUrl)
                    return True,self.meetingKey
                    
            else:
                if (self.serviceType == MeetingConstants.TrainingCenter):
                    afterScheduleMeetingReturnResult = str(self.myDriver.page_source)
                    self.meetingKey = self.parseMeetingKey(afterScheduleMeetingReturnResult)
                    return True,self.meetingKey
        else:
            return False,'switch service fail'            
#         return self.meetingKey
    
    def getRealMeetingTopic(self):
        """return real meeting topic
        @return: meeting topic when switch successfully,otherwise return ''
        @rtype: string
        """
        return self.realmeetingTopic
    
    def parseMeetingKey(self,response):
        """Parse meeting key by schedule meeting response.
        @param response: schedule meeting response
        @type response: string
        @return: meeting key when switch successfully,otherwise return ''
        @rtype: string   
        """
        index = -1
        start = -1
        if (self.serviceType == MeetingConstants.SupportCenter):
            index = response.find('SN=')
        else:
            index = response.find('MK=')
        if (index == -1):
            self.log.fdbg(os.path.normpath(__file__) + '==>parseMeetingKey : index == -1')
            return ''
        start = index + 3
    
        if (start == -1):
            self.log.fdbg(os.path.normpath(__file__) + '==>parseMeetingKey : start == -1')
            return ''
        
        meetingKey = ''
        for i in range(start, len(response)):
            if (response[i].isdigit()):
                meetingKey = meetingKey + response[i]
            else:
                break

        return meetingKey    
    
    def startMeeting(self,meetingKey = '',jmtFlag = False):
        """Start a meeting by valid account and meeting key.
        @param meetingKey: Meeting number in meeting info page
        @type meetingKey: string
        @return: True when switch successfully,otherwise return False and error message
        @rtype: tuple     
        """
#         self.__jmtData._start_time =  time.time()
#         return True
    
        meetingKey = self.meetingKey
        
        if (meetingKey == ''):
            if self.scheduleMeeting()[0] :
                meetingKey = self.scheduleMeeting()[1]
        
        res = self.loginSite(self.acount)[0]
        if (not res):
            self.log.fdbg(os.path.normpath(__file__) + '==>startMeeting : self.loginSite(acount)res = False')
            return False,'startMeeting : self.loginSite(acount)res = False'

        if (self.serviceType != MeetingConstants.EventCenter):
            res = self.switchService(self.serviceType)[0]
            if (not res):
                self.log.fdbg(os.path.normpath(__file__) + '==>startMeeting : self.switchService()res = False')
                return False,'startMeeting : self.switchService()res = False'
        
        if (self.serviceType == MeetingConstants.EventCenter):
            startAction = "TE"
            mkParam = '&MK=' + meetingKey
        elif (self.serviceType == MeetingConstants.SupportCenter):
            startAction = "HS"
            mkParam = '&SN=' + meetingKey
        else:
            startAction = "HM"
            mkParam = '&MK=' + meetingKey
            
        url = self.siteUrl + 'm.php?AT=' + startAction + mkParam #'https://pl.qa.webex.com/fr26java2/m.php?AT=HM&MK=' + meetingKey
#         print 'start meeting url=', url
        self.log.fdbg(os.path.normpath(__file__) + '==>startMeeting : url = ' + url)
        self.myDriver.get(url)
        try:
            currentUrl=str(self.myDriver.current_url)
        except Exception,e:
            self.log.fdbg(os.path.normpath(__file__) + '==>get meeting  Url exception message :' + str(e))
        self.log.fdbg(os.path.normpath(__file__) + '==>after start meeting  Url' + currentUrl)
        #time.sleep(2)
        if isWindows():
            from common.win.wStdWindow import PyWinWindow
            from common.PyWindow import mouseOperateOnWindow,getChildWindowListByClass
            import win32gui as win32
            from common.input import mouseClick,mouseMove
            if self.browserName.lower() == 'ie' and self.downloadType.lower() in ['activex','tfs'] and not jmtFlag :
                tryTimes = 0
                installButtonList = []
                oBrowser =  []
                windowsList=getChildWindowListByClass(win32.GetDesktopWindow(),'',20,False,None)#find broswer object
                for window1 in windowsList:
                    for pid1 in self.getBrowserPID():
                        if window1.getProcessId() == int(pid1):
                            oBrowser.append(window1)
                if 0 != len(oBrowser):
                    while len(installButtonList) == 0 and tryTimes <= 30:
                        for pyWinBrowser in oBrowser:
                            if pyWinBrowser.getClassName() == "IEFrame": #find  IE main window object
                                installButtonList = getChildWindowListByClass(pyWinBrowser.getHandle(),
                                                                              'Frame Notification Bar',20,False,None)
                                if 0 != len(installButtonList):
                                    break
                        time.sleep(1)
                        tryTimes = tryTimes + 1
                else:
                    self.log.fdbg(os.path.normpath(__file__) + '==> no find IE browser')
                    return False,'no find IE browser'
                    
                if len(installButtonList) == 0 :
                    self.log.fdbg(os.path.normpath(__file__) + '==> no find the first install button'+
                                  ' when download type is activex or no find run button when download type is TFS')
                    self._jmtData._start_time =  time.time()#when replace dll,can not find install button
                    return False,'no find the first install button' 
                
                if self.downloadType.lower() == 'activex':
                    mouseClick(installButtonList[0].getRect().left+900, installButtonList[0].getRect().bottom-20)
                    time.sleep(2)
                    tryTimes = 0
                    installButtonList2 = []
                    warningWindow = []
                    while len(warningWindow) == 0 and tryTimes <= 30:
                        warningWindow = getChildWindowListByClass(win32.GetDesktopWindow(),'#32770',20,False,None)
                        if 0 != len(warningWindow):
                            installButtonList2 = getChildWindowListByClass(warningWindow[0].getHandle(),'Button',20,False,None)
                        if len(installButtonList2) != 0:
                            for i in installButtonList2:
                                if  i.getText() =='&Install':
                                    time.sleep(1)
                                    self._jmtData._start_time =  time.time()
                                    return mouseOperateOnWindow(i),''
                        time.sleep(1)
                        tryTimes = tryTimes + 1
                    else:
                        self.log.fdbg(os.path.normpath(__file__) + '==> no find the warning window when download type is activex')
                        return False,'no find the warning window when download type is activex'
                elif self.downloadType.lower() == 'tfs' :
                    self._jmtData._start_time =  time.time()
                    return mouseClick(installButtonList[0].getRect().left+755, installButtonList[0].getRect().bottom-20),''
                        
            elif self.browserName.lower() == 'firefox':
                pass
            
        
        self._jmtData._start_time =  time.time()
        return True,''    
    def joinMeeting(self,languageId,localeId, meetingKey):
        """Join a in progress meeting by valid account and meeting key.
        @param languageId: language ID
        @type languageId: string
        @param localeId: locale Id
        @type localeId: string
        @param meetingKey: Meeting number in meeting info page
        @type meetingKey: string
        @return: True when switch successfully,otherwise return False
        @rtype: boolean     
        """
        if (meetingKey == ''):
            self.log.fdbg(os.path.normpath(__file__) + '==>joinMeeting : meetingKey = ""')
            return False
        
        
        self.switchLanguage(languageId,localeId,False)
        
          
        res = self.switchService(self.serviceType)
        if (not res):
            self.log.fdbg(os.path.normpath(__file__) + '==>joinMeeting : self.switchService()res = False')
            return False
        
        if (self.serviceType == MeetingConstants.EventCenter):
            joinAction = "JE"
            attendeeNameParam = '&FN=' + self.acount.firstName + '&LN=' + self.acount.lastName
            mkParam = '&MK=' + meetingKey
            pwParam = '&PW=' + self.meetingPassword
            emParam = '&AE=' + self.acount.mailAddress
        elif (self.serviceType == MeetingConstants.SupportCenter):
            joinAction = 'JS'
            attendeeNameParam = '&FN=' + self.acount.firstName + '&LN=' + self.acount.lastName
            mkParam = '&SN=' + meetingKey
            pwParam = ''
            emParam = '&EM=' + self.acount.mailAddress
        else:
            joinAction = "JM"
            attendeeNameParam = '&AN=' + self.acount.firstName + ' ' + self.acount.lastName
            mkParam = '&MK=' + meetingKey
            pwParam = '&PW=' + self.meetingPassword
            emParam = '&AE=' + self.acount.mailAddress
            
        url = self.siteUrl + 'm.php?AT=' + joinAction + mkParam + pwParam + attendeeNameParam + emParam
        self.log.fdbg(os.path.normpath(__file__) + '==>joinMeeting : url = ' + url)
        self.myDriver.get(url) 
        if (not res):
            self.log.fdbg(os.path.normpath(__file__) + '==>joinMeeting : webbrowser.open(url)res = False')
            return False

        self._jmtData._start_time =  time.time()

    def stopMeeting(self):
        """kill meeting process.
        @return: True when stop meeting successfully,otherwise return False and message
        @rtype: tuple     
        """
        
        if isWindows() :
            toKillProccessList = ["IEDriverServer.exe","chromedriver.exe"]
            resultlist = []
            if self.serviceType.lower() == "mc" or self.serviceType.lower() == "ec" or self.serviceType.lower() == "tc" :
                toKillProccessList.append("atmgr.exe")
            elif self.serviceType.lower() == "sc":
                toKillProccessList.append("atscmgr.exe")
                toKillProccessList.append("OUTLOOK.EXE")
            for processName in toKillProccessList:
                p=subprocess.Popen(("taskkill /f /im " + processName),shell=True)
                ret = p.wait()
                resultlist.append(ret)
            for resultT in resultlist:
                if resultT not in [0]:
                    return False,'stop meeting fail'
            return True,''
        elif isMacOSX():
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
        
            return True,''
        
    def getBrowserPID(self):
        """return webdriver process ID
        @return: browser process ID
        @rtype: int
        """
        if self.browserName.lower() == "firefox":
            return self.myDriver.binary.process.pid
        elif self.browserName.lower() == "ie":
            if isWindows():
                s  = 'iexplore.exe'
                im = '"IMAGENAME eq %s"'%s
                cmd = "tasklist /NH /FI %s"%im
                cmd = '''for /f \"tokens=2 delims=,"'''+''' %F'''+" in ('tasklist /nh /fi %s"%im+" /fo csv') do @echo %~F"
                s = os.popen(cmd).read()
                pidlist = s.split("\n")
#                 print "filter(None, pidlist)",filter(None, pidlist)
                return filter(None, pidlist)
        
        
        
class Acount(object):
    
    def __init__(self, userName, password, firstName, lastName, mailAddress):
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.mailAddress = mailAddress

class TelephoneInfo(object):
    def __init__(self, config, description, tspAcount):
        self.config = config
        self.description = description
        self.tspAcount = tspAcount
        
    def getConfigParam(self):
        param = ""
        if (self.config != ""):
            param = '&TC=' + str(self.config)
        
        return param
    
    def getDescriptionParam(self):
        param = ""
        if (self.description != ""):
            param = '&TD=' + str(self.description)
            
        return param
        
    def gettspAcountParam(self):
        param = ""
        if (self.description != ""):
            param = '&TA=' + str(self.tspAcount)
            
        return param

def main():
    """debug function """   
#     siteUrl = 'https://hl2demo.qa.webex.com/t1wdta03' 
#     userName = 'tauser'
#     password = 'P@ss123ta'
#     serviceType = MeetingConstants.MeetingCenter
    
    siteUrl = 'https://t1wdta03.qa.webex.com/t1wdta03'
    userName = 'tauser'
    password = 'P@ss123'
    serviceType = MeetingConstants.MeetingCenter
    languageId = PyLanguageId.SimplifiedChinese
    localeId = PyLocaleId.US
    meetPassword = '111111!aA'
    firstName = 'william'
    lastName = 'sun'
    mailAddress = 'williamsun@qa.webex.com'
    acount = Acount(userName, password, firstName, lastName, mailAddress)
    teleInfo = TelephoneInfo('1', 'dd', '')
    #self, siteUrl,browserName,serviceType,acount,meetingPassword,teleInfo,meetingTopic
    preMeeting = wbxMeeting(siteUrl,'','ie',serviceType,acount,meetPassword,teleInfo,'TA for mac  EC','gfghfgh')
#     Meeting.setLanguage('1')
    
    preMeeting.setTelephoneConfig(teleInfo)
          
    print"login result==", preMeeting.loginSite(acount)
#     
    print "switch Service result ===", preMeeting.switchService(serviceType)
 
    mk=preMeeting.scheduleMeeting()
    print "mk===",mk
# #     print"switch Language result=====", preMeeting.switchLanguage(languageId, localeId, True)
#     preMeeting.switchLanguage(languageId, localeId, True)   
    preMeeting.startMeeting(jmtFlag = True)
    preMeeting.stopMeeting()
#     preMeeting.clearWebexPackage()
#     preMeeting.startMeeting("333444")
#     time.sleep(15)
    preMeeting.closeBrowser()

#    preMeeting.joinMeeting(acount, mk)
#     preMeeting.logoutMeeing()
# main()
