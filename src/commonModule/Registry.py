from common import isMacOSX,isWindows


def set_reg(REG_PATH ,name , valueType,value ):
#     print "value = ",value
    if isWindows():
        import _winreg
        if REG_PATH.split("\\")[0] == "HKEY_LOCAL_MACHINE":
            rootName = _winreg.HKEY_LOCAL_MACHINE
            
        elif REG_PATH.split("\\")[0] == "HKEY_CLASSES_ROOT":
            rootName = _winreg.HKEY_CLASSES_ROOT
            
        elif REG_PATH.split("\\")[0] == "HKEY_CURRENT_USER":
            rootName = _winreg.HKEY_CURRENT_USER
            
        elif  REG_PATH.split("\\")[0] == "HKEY_USERS":
            rootName = _winreg.HKEY_USERS
            
        elif  REG_PATH.split("\\")[0] == "HKEY_CURRENT_CONFIG":
            rootName = _winreg.HKEY_CURRENT_CONFIG
            
        else:
            rootName = ""
            REG_PATH = ""
            print "no find root name :", REG_PATH.split("\\")[0]
        REG_PATH = REG_PATH[len(REG_PATH.split("\\")[0]) + 1:]
        
        try:
            _winreg.CreateKey(rootName, REG_PATH)
            registry_key = _winreg.OpenKey(rootName, REG_PATH, 0, 
                                           _winreg.KEY_WRITE)
            if valueType == "REG_SZ":
                _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
            else:
                _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_DWORD, value)
            _winreg.CloseKey(registry_key)
            return True
        except WindowsError,e:
            print "set regitry,error is :",e
            return False
    elif isMacOSX():
        import plistlib
        try:
            plHandle = plistlib.readPlist(REG_PATH)
            if name in plHandle:
                if plHandle[name] == value :
                    print "have exist " + name + ":" + value
                    return
            tempDict[name] = value
            plistlib.writePlist(tempDict, REG_PATH)
            return True
        except Exception,e:
            print "set_reg error ,message :",e
            return False
        

def get_reg(REG_PATH ,name ):
    if isWindows():
        import _winreg
        if REG_PATH.split("\\")[0] == "HKEY_LOCAL_MACHINE":
            rootName = _winreg.HKEY_LOCAL_MACHINE
            
        elif REG_PATH.split("\\")[0] == "HKEY_CLASSES_ROOT":
            rootName = _winreg.HKEY_CLASSES_ROOT
            
        elif REG_PATH.split("\\")[0] == "HKEY_CURRENT_USER":
            rootName = _winreg.HKEY_CURRENT_USER
            
        elif  REG_PATH.split("\\")[0] == "HKEY_USERS":
            rootName = _winreg.HKEY_USERS
            
        elif  REG_PATH.split("\\")[0] == "HKEY_CURRENT_CONFIG":
            rootName = _winreg.HKEY_CURRENT_CONFIG
            
        else:
            rootName = ""
            REG_PATH = ""
            print "no find root name :", REG_PATH.split("\\")[0]
        REG_PATH = REG_PATH[len(REG_PATH.split("\\")[0]) + 1:]

        try:
            registry_key = _winreg.OpenKey(rootName, REG_PATH, 0,
                                           _winreg.KEY_READ)
            value, regtype = _winreg.QueryValueEx(registry_key, name)
            _winreg.CloseKey(registry_key)
            return value
        except WindowsError,e:
            print "get_reg error,message : ",e
            return None
            
    elif isMacOSX():
        import plistlib
        try:
            plHandle = plistlib.readPlist(REG_PATH)
            return plHandle[name]
        except Exception,e:
            print "get_reg error,message :",e
            return None
# if __name__ == "__main__" :
#     print "get_reg === ",get_reg() 