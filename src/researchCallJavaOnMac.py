'''
Created on Mar 14, 2016

@author: sky
'''
import subprocess
import os

def EXEC_CMD(cmd, check_output_str = '',check_return = False):
    bSuccess = False
    try:
        p = subprocess.Popen(cmd, bufsize = -1,shell=False,stdout=subprocess.PIPE)
        (stdoutdata, stdindata) = p.communicate(None)
        ret = p.returncode
        stdindata#remove the warning about 'stdindata' not used
        if 0 == ret:
            if '' == check_output_str or None == check_output_str:
                bSuccess = True
            else:
                if -1 != stdoutdata.find(check_output_str):
                    bSuccess = check_return
                else:
                    bSuccess = not check_return

    except Exception,e:
        print e
        
    return bSuccess

def __runMBJavaAPI(infoFile, fileType):
        try:
            localJobPath = r'/Users/sky/Documents/client_mb_job'
            mbAPIJarPath = r'/Users/sky/Library/MagicBoat/SDK/Java/MagicBoatSDK.jar' 
            mbAPIClassName = 'AutoMBJob'                    
            javaCmd = r'java -cp %s;%s %s %s %s' % (localJobPath, mbAPIJarPath, mbAPIClassName, infoFile, fileType)
            ret = os.popen(javaCmd).readlines()
#             TALog.fdbg(str(ret))
            print ret
        except Exception,e:
#             TALog.fdbg(str(e))
            print e
            
        return ret
if __name__ == "__main__":
    importZipFileName = r'/Users/sky/Documents/client_mb_job/Mac_Python_iMagic_WebExClient.zip'
    __runMBJavaAPI(importZipFileName, '1')
    __runMBJavaAPI(r'/Users/sky/Library/MagicBoat/client_mb_job/20160314031715_Mac_EC_BVT.txt',2)
    
    if 0 != 0:
        _root = '/Users/sky/Library/MagicBoat'
        MAGICBOAT_SDK = '/Users/sky/Library/MagicBoat/SDK/Java/MagicBoatSDK.jar'
        MAGICBOAT_JOB_LAUNCHER_NAME = 'mbjob'
        _job_config = 'C:\Users\Administrator\magicboat\workspace\DS_Sharing-20151216143001.xml'
        _str_libs = ''
        _bridge_log_file = 'C:\Users\Administrator\magicboat\abcdefg.log'
        _workspace = ''
        EXEC_CMD(r'javaw -cp "%s;%s" %s "%s" "%s" "%s"' % (_root, MAGICBOAT_SDK, MAGICBOAT_JOB_LAUNCHER_NAME, _job_config, _str_libs, _bridge_log_file))
        _report_file = _workspace + os.sep + os.path.splitext(os.path.basename(_job_config))[0] + ".zip"
        if os.path.exists(_report_file):
            print 'copy file!!!!'
        else:
            print 'No report file exist, if you job executed successfully, please make sure job launched as expected and "java[w].exe" for API job not be closed unexpected.'