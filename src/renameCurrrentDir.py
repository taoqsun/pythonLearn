#-*- coding: UTF-8 -*-
import os
import time
import random

currentDir = os.path.dirname(__file__) 
print "current directory === > ",currentDir
flagItem = random.randint(11,9999999)
def renameDir(oldDir="",dirValue=""):
    global flagItem
    fileList = os.listdir(dirValue)
    print "file list == >",fileList
    logfile = currentDir + "/" + \
              time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".log"
    file_handle = open(logfile,"a+")
    for item in fileList:
        
        if os.path.isfile(dirValue+os.sep+item) and item[item.find('.'):] not in [".py",".pyc" ,".log"]:
            
            
            if oldDir != "":
                file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +
                                        " -- " + oldDir + '\\' + str(item) +"====>"+ str(flagItem) + "\n")
            else:
                file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +
                                        " -- " + str(item) +"====>"+ str(flagItem) + "\n")
            dirHead = dirValue + os.sep
            try: 
                os.rename(dirHead + item, dirHead + str(flagItem))
            except Exception,e:
                file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+
                                        " -- " + str(e) + "\n")
            flagItem = flagItem + random.randint(11,999)
            
        if os.path.isdir(dirValue+os.sep+item):
            newDir = dirValue+os.sep+str(flagItem)+str(random.randint(11,999))
            file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+
                                        " -- " + dirValue + os.sep +item + '===>'+newDir+"\n")
            os.rename(dirValue+os.sep+item,newDir)
            renameDir(dirValue+os.sep+item,newDir)

    file_handle.close()
def renameDirFromLog(dirValue=""):
    fileList = os.listdir(dirValue)
    for item in fileList:
        if os.path.isfile(item):
            logfile = currentDir + "/" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".log"
            file_handle = open(logfile,"a+")
            file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + 
                                   " -- " + str(dirValue+os.sep+item) +"====>"+ str(flagItem) + "\n")
            file_handle.close()
    #         os.c(item, flagItem)
            flagItem = flagItem + 1
            print "file ==> ",dirValue+os.sep+item
            
        if os.path.isdir(item):
            print "dir ==> ",dirValue+os.sep+item
            print os.path.abspath(os.path.dirname(item))+os.sep+item
            renameDir(os.path.abspath(os.path.dirname(item))+os.sep+item)
    
renameDir(dirValue=currentDir)       
