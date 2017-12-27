'''
Created on Sep 20, 2017

@author: Administrator
'''
import ConfigParser
from ConfigParser import NoSectionError
import os
from cilogger import createLogger
log = createLogger()

class INIFileHandle():
    
    def __init__(self,INIfilePath):
        self.filePath = INIfilePath
        self.Config = ConfigParser.ConfigParser()
    
    def getSectionMap(self,setionName):
        dictOption = {}
        try:
            options = self.Config.options(setionName)
        except NoSectionError:
            log.fdbg("%s is not exist,please check."%setionName) 
            return dictOption
        for option in options:
            try:
                dictOption[option] = self.Config.get(setionName, option)
                if dictOption[option] == -1:
                    log.fdbg("skip: %s" % option)
            except:
                log.fdbg("exception on %s!" % option)
                dictOption[option] = None
        return dictOption
    
    def getFileContents(self):
        dictFileContents = {}
        if not os.path.exists(self.filePath):
            log.fdbg("INIFileHandle : can not find  %s ,please check." % self.filePath)
            return dictFileContents
        self.Config.read(self.filePath)
        for sectionItem in self.Config.sections():
            dictFileContents[sectionItem] = self.getSectionMap(sectionItem)
        return dictFileContents
    
    def deleteIniFile(self,inifilepath):
        log.fdbg("delete the %s file in first meeting:" % inifilepath)
        if os.path.exists(inifilepath):
            os.remove(inifilepath)
        log.fdbg("delete webex.ini file success")
    