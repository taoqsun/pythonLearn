
'''
Created on Mar 31, 2016

@author: Administrator
'''

import _winreg
import os

def readRegistry(keyPath = r"SOFTWARE\python",keyName = "",valueList = []):
    asubkey_value = None
    try:
        aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
        aKey = _winreg.OpenKey(aReg, keyPath)
        if aKey and aReg :
            currentKeyName = os.path.basename(keyPath)
            if "" != keyName:
                if str(currentKeyName).lower() == keyName.lower() and "" != currentKeyName:
                    if 0 != _winreg.QueryInfoKey(aKey)[1]:
                        for i in range(_winreg.QueryInfoKey(aKey)[1]):
                            try:
                                asubkey_value=_winreg.EnumValue(aKey,i)
                                if len(asubkey_value) != "":
                                    valueList.append(asubkey_value)
                            except Exception,e:
                                print " get asubkey_value error message = ",e
                    else:
                        print keyName + " have not any values!!!"
                else:
                    if 0 != _winreg.QueryInfoKey(aKey)[0] : 
                        for i in range(_winreg.QueryInfoKey(aKey)[0]):
                            subKeyName = _winreg.EnumKey(aKey,i)
                            readRegistry(os.path.join(keyPath,subKeyName),keyName,valueList)
            else:
                if 0 != _winreg.QueryInfoKey(aKey)[1]:
                    for i in range(_winreg.QueryInfoKey(aKey)[1]):
                        try:
                            asubkey_value=_winreg.EnumValue(aKey,i)
                            if len(asubkey_value) != "":
                                valueList.append(asubkey_value)
                        except Exception,e:
                            print " get asubkey_value error message = ",e
                else:
                    print keyName + " have not any values!!!"
        else:
            print "connect registry or open key is failed!!!"
        if len(valueList) != 0:
            return valueList
    except Exception,e:                                               
        print "error message = ",e
    finally:
        _winreg.CloseKey(aKey)                                                  
        _winreg.CloseKey(aReg)
# SOFTWARE\Python\PythonCore\2.7\PythonPath
def writeRegistry(keyName = "MyNewKey",keyData = r"C:\Windows\explorer.exe",KeyPath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"):
    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
    aKey = _winreg.OpenKey(aReg , KeyPath , 0, _winreg.KEY_WRITE)
    try:   
        _winreg.SetValueEx(aKey,keyName,0, _winreg.REG_SZ,keyData) 
    except EnvironmentError:                                          
        print "Encountered problems writing into the Registry..."
    _winreg.CloseKey(aKey)
    _winreg.CloseKey(aReg)

print readRegistry(keyPath=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",keyName="",valueList= [])

settingValue = "\"" + readRegistry(keyPath=r"SOFTWARE\Python\PythonCore\2.7\InstallPath",keyName="",valueList= [])[0][1] + \
            "python.exe\" C:\client_mb_job\\auto_MB_Client.py "

print settingValue

for keyValue in readRegistry(keyPath=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",keyName=""):
    if keyValue[1] == settingValue :
        print "true"
        break
        
# writeRegistry(keyData = "\"" + readRegistry(keyPath=r"SOFTWARE\Python\PythonCore\2.7\InstallPath",keyName="")[0][1] +"python.exe\" C:\client_mb_job\\auto_MB_Client.py " ) 
# print readRegistry2()

           
