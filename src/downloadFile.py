'''
Created on Sep 24, 2015

@author: taoqsun
'''
import urllib
import os

if __name__ == '__main__':
    try:
        urllib.urlretrieve("https://hjt31.qa.webex.com/client/T31L/Cisco_WebEx_Add-On.exe?v=31.0.0.1439","C:\\Cisco_WebEx_Add-On.exe")
    except IOError,e:
        pass
    finally:
        os.system("C:\\Cisco_WebEx_Add-On.exe")