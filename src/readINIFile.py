'''
Created on Sep 20, 2017

@author: Administrator
'''
import ConfigParser
from ConfigParser import NoSectionError
import os

class INIFileHandle():
    
    def __init__(self,INIfilePath):
        self.filePath = INIfilePath
        self.Config = ConfigParser.ConfigParser()
    
    def getSectionMap(self,setionName):
        dictOption = {}
        try:
            options = self.Config.options(setionName)
        except NoSectionError:
            print "%s is not exist,please check."%setionName
            return dictOption
        for option in options:
            try:
                dictOption[option] = self.Config.get(setionName, option)
                if dictOption[option] == -1:
                    print "skip: %s" % option
            except:
                print "exception on %s!" % option
                dictOption[option] = None
        return dictOption
    
    def getFileContents(self):
        dictFileContent = {}
        if not os.path.exists(self.filePath):
            return dictFileContent
        self.Config.read(self.filePath)
        for sectionItem in self.Config.sections():
            dictFileContent[sectionItem] = self.getSectionMap(sectionItem)
        return dictFileContent
    
    
    
if __name__=="__main__":
    INIInstence = INIFileHandle("C:\ProgramData\WebEx\siteinfo.ini")
    print INIInstence.getFileContents()
    print INIInstence.getSectionMap("gota201.eng.webex.com")