'''
Created on Oct 28, 2015

@author: sky
'''
import subprocess
# from subprocess import Popen
# def clearWebexPackage(self):
#         """clear webex package
#         @return: operation result
#         @rtype: boolean
#         """
#         result=False
# #         subprocess.Popen('rd /s /q C:\ProgramData\Webex,C:\Users\Administrator\AppData\LocalLow\Webex,C:\Users\Administrator\AppData\Local\Webex,C:\Users\Administrator\AppData\Local\Webex',shell=True)
#         subprocess.Popen('rd /s /q C:\Users\Administrator\AppData\Local\Webex',shell=True)
#         subprocess.Popen('rd /s /q C:\ProgramData\Webex,C:\Users\Administrator\AppData\LocalLow\Webex',shell=True) 
#         subprocess.Popen('rd /s /q C:\ProgramData\Webex,',shell=True)
#         if Popen.wait() == 0:
#             result=True


# subprocess.Popen('rd /s /q \"C:\Windows\Downloaded Program Files\"',shell=True)
subprocess.Popen('rmdir /s /q C:\\500',shell=True)