'''
Created on Oct 28, 2015

@author: sky
'''
import os
print os.path.dirname("c:\Down\dd")
print os.path.dirname("https://t1wdta03.qa.webex.com/t1wdta03")
mountFilePath = "C:\Users\Administrator\Downloads\workspace"
fileList = []
for (dirpath, dirnames, filenames) in os.walk(mountFilePath):
    fileList.extend(filenames)
    break
print fileList