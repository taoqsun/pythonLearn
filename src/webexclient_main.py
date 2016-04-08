'''
Created on 2014-1-7

@author: haosu
'''
import os
import time
import sys
import types
import shutil
import subprocess, signal

def iswindows():
    if os.name.startswith('nt'):
        return True
    
    return False

__iswindows__ = iswindows()

def ismacosx():
    if os.name.startswith('posix') and sys.platform.startswith('darwin'):
        return True
    
    return False

__ismacosx__ = ismacosx()

def getCurrentScriptPath(): 
    try:   
        _cur_file = __file__
    except Exception: #NameError
        _cur_file = sys.path[0]
        
    return os.path.dirname(os.path.realpath(_cur_file))

class Logger():
    def __init__(self, log_file_path = ''):
        self.__fhandle = None
        try:
            if not os.path.exists(log_file_path):
                print 'Logger: file path not exist "%s" , create log directory at' % log_file_path
                os.makedirs(log_file_path)
            self.__logFile = log_file_path + os.sep + os.path.basename(__file__) + "-%s" % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
#             print self.__logFile
            self.__fhandle = open(self.__logFile + '.log',"wb")
        except Exception,eMsg:
            print 'Logger Exception: "%s" ' % str(eMsg)
    
    def getLogFileName(self):
        return self.__logFile
    
    def endLog(self):
        try:
            if None != self.__fhandle:
                self.__fhandle.close()
                self.__fhandle = None
        except:
            pass
              
    def __del__(self):
        self.endLog()
        
    def clean(self):      
        if None!=self.__fhandle:
            self.__fhandle.write("")        
    
    def __construct_output_msg(self, log_str,msg_type = 'I'):
        logstr = log_str
        str_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if 'I' == msg_type.upper():
            logstr = str_time  + " -- %s" % (str(log_str))
        elif 'W' == msg_type.upper():
            logstr = str_time  + " -- %s %s" % ('WARNING:', str(log_str))
        elif 'E' == msg_type.upper():
            logstr = str_time  + " -- %s %s" % ('ERROR:', str(log_str))
            
        return logstr
    
    def dbg(self,log_str,msg_type = 'I'):
        print self.__construct_output_msg(log_str, msg_type)  
        
    def fdbg(self,log_str,msg_type = 'I',output_to_stdout = True):
        str_msg = self.__construct_output_msg(log_str, msg_type) 
        if output_to_stdout == True:
            sys.stdout.writelines(str_msg + os.linesep)                       
        if self.__fhandle!=None:
            self.__fhandle.writelines(str_msg + os.linesep)
            self.__fhandle.flush()
            
SCRIPT_HOME = getCurrentScriptPath()
log = Logger(os.path.join(SCRIPT_HOME,'Logs'))

import datetime

def cleanHistories(root_dir, extensions = ['*'], days_to_keep = 7, excludes = [], include_sub_dir = True):
    if not isinstance(extensions, types.ListType) or not isinstance(days_to_keep, types.IntType) \
        or not isinstance(excludes, types.ListType) or not isinstance(include_sub_dir, types.BooleanType):
        log.fdbg('cleanHistories() invalid parameters %s, %s, %d, %s, %s' % (root_dir,str(extensions),days_to_keep,str(excludes),str(include_sub_dir)))
        return False
    
    if 0 ==len(extensions):
        return False
    
    _check_all_items = '*' in extensions
    _cur_tm = time.localtime(time.time())
    for _fItem in os.listdir(root_dir):
        if not _check_all_items and os.path.splitext(_fItem)[1].lower().strip() not in extensions:
            continue
        
        b_contain_exclude_str = False
        for _exclude_item in excludes:
            if -1 != _fItem.find (_exclude_item) :
                b_contain_exclude_str = True
                break
            
        if b_contain_exclude_str:
            continue
        
        _abs_fItem = os.path.join(root_dir,_fItem)
        _days = _cur_tm.tm_yday        
        _f_tm = time.localtime( os.path.getmtime(os.path.join(root_dir,_fItem)) )
        _years =  _cur_tm[0] - _f_tm[0]
        for _year in range(1,_years+1):
            dt = datetime.datetime(_cur_tm.tm_year - _year,12,31)
            _t = dt.timetuple()
            _days += _t.tm_yday
        _days -= _f_tm.tm_yday
        
        if os.path.isdir(_abs_fItem) and include_sub_dir:
            cleanHistories(_abs_fItem, extensions, days_to_keep, excludes, include_sub_dir)
            if 0 == len(os.listdir(_abs_fItem)) or _days > days_to_keep:
                log.fdbg('remove empty folder %s' % _abs_fItem)
                os.rmdir(_abs_fItem)
        elif os.path.isfile(_abs_fItem) and _days > days_to_keep:
                log.fdbg('remove time over file : %s' % _abs_fItem)
                os.remove(_abs_fItem)
                
    return True

def addenv(varname,newvalue):
    try:
        temp = os.environ[varname] + ';'
    except Exception,e:
        temp = ''
        log.dbgInfo(str(e))
    finally:
        os.environ[varname] = temp + newvalue
        
def EXEC_CMD(cmd, check_output_str = '',check_return = False,output = None):
    bSuccess = False
    try:
        p = subprocess.Popen(cmd, bufsize = -1,shell=True,stdout=subprocess.PIPE)
        (stdoutdata, stdindata) = p.communicate(None)
        ret = p.returncode
        stdindata#remove the warning about 'stdindata' not used
        if None != output and isinstance(output,types.ListType):
            output.append(stdoutdata)

        if 0 == ret:
            if '' == check_output_str or None == check_output_str:
                bSuccess = True
            else:
                if -1 != stdoutdata.find(check_output_str):
                    bSuccess = check_return
                else:
                    bSuccess = not check_return

    except Exception,e:
        log.fdbg( 'EXEC_CMD(%s) \r\n\t Exception:%s' % (cmd,str(e)),'E')
 
#     log.logInfo("Execute '" + cmd + "' result: " + str(bSuccess))
    return bSuccess

def STAFCopyToRemoteMachine(src, remote_IP, dest):
    if not isinstance(remote_IP, types.StringTypes) or not isinstance(dest, types.StringTypes):
        return False
    
    if ''==remote_IP or ''==dest:
        return False
    
    if os.path.isdir(src):
        staf_cmd_str = "staf local fs copy DIRECTORY %s TODIRECTORY %s TOMACHINE %s RECURSE" % (src, dest, remote_IP)
    elif os.path.isfile(src):
        staf_cmd_str = "staf local fs copy FILE %s TODIRECTORY %s TOMACHINE %s" % (src, dest, remote_IP)
    else:
        return False
    
    return EXEC_CMD(staf_cmd_str,'RC:')

 

DELETE_FILE = 0X0002
DELETE_DIR = 0X0004
DELETE_ALL = 0X0006

def deleteItemsInDirectory(target_dir, option = DELETE_ALL, excludeNameList = [],del_root_dir = False): 
    if not os.path.exists(target_dir):
        log.dbgInfo(target_dir + ' not exist')
        return
    try:
        for f in os.listdir(target_dir):
            targetFile = os.path.join(target_dir, f)
            if f in excludeNameList:
                continue
            if os.path.isfile(targetFile) and (option & DELETE_FILE):  
                os.remove(targetFile)  
            elif os.path.isdir(targetFile) and (option & DELETE_DIR):
                shutil.rmtree(targetFile)

        if del_root_dir and  0 == len(os.listdir(target_dir)):
            shutil.rmtree(target_dir)
    except Exception, e: 
        log.fdbg('deleteItemsInFolder() Exception: ' + str(e),'E')

from zipfile import ZipFile

def unzipFile(srcZipFile,dest_folder):
    if not os.path.isfile(srcZipFile):
        return False    
    zf = ZipFile(srcZipFile)
    NameList = zf.namelist();
    for nameItem in NameList:
        zf.extract(nameItem,dest_folder)
    zf.close()
    return True
        
def checkProcessAndKill(process_name):
    try:
        processList = []
        if __iswindows__:
            EXEC_CMD('tasklist','',False,processList)
        elif __ismacosx__:
            EXEC_CMD('ps -A','',False,processList)
        else:
            log.fdbg("can not kill " + str(process_name) +" process on unknown OS")
        processList = '\n'.join(processList)
        for line in filter(None, processList.splitlines()):
            if process_name in line:
                if __ismacosx__:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
                elif __iswindows__:
                    pid = int(line.split(None)[1])
                    os.kill(pid, signal.SIGTERM)
    except Exception,e:
        log.fdbg(str(e))
    

MAGICBOAT_SDK = 'C:\Program Files\Cisco Webex\MagicBoat\SDK\Java\MagicBoatSDK.jar'
MAGICBOAT_JOB_LAUNCHER_NAME = 'mbjob'


def scanFileInFolder(folder, extension, excludes, include_sub_folder, output_list):
    if not os.path.exists(folder):
        log.fdbg('Folder for scan not exist(%s)' % folder)
        return False
    
    if (None !=excludes and not isinstance(excludes,types.ListType)) or not isinstance(output_list, types.ListType):
        return False
    
    fItems =  os.listdir(folder)
    for _fItem in fItems:
        _real_fItem = os.path.join(folder, _fItem)
        if os.path.isfile(_real_fItem) and '' != extension and os.path.splitext(_real_fItem)[1].lower().strip() != extension.lower().strip():
            continue
        
        b_contain_exclude_str = False
        if None != excludes:   
            for _exclude_item in excludes:
                if -1 != _fItem.find (_exclude_item) :# if file name contain excluded string
                    b_contain_exclude_str = True
                    break
            
        if b_contain_exclude_str:
            continue
        
        if  os.path.isfile( _real_fItem ):
            output_list.append( _real_fItem )
        elif include_sub_folder:
            scanFileInFolder(_real_fItem, extension, excludes,include_sub_folder, output_list)
        
    return True

if __name__ == "__main__":
    checkProcessAndKill('vnc-E4_6_3-x86_win32_view')
    if 0 != 0:
        log.fdbg('Command line parameters: %d %s' % (len(sys.argv), str(sys.argv)))
        if len(sys.argv) < 4:
            log.fdbg( 'Invalid parameters specified.')
            exit()
        
        _jenkins_ip = sys.argv[1]
        _report_folder = sys.argv[2]
        _cfg_files = sys.argv[3].split(';')
        _bridge_log_file = log.getLogFileName() + '-mbjob.log'
        cleanHistories(os.path.join(SCRIPT_HOME,'Logs'))
        for i in range(0,1):
            i
            checkProcessAndKill("AutoIt3.exe")
            _root = getCurrentScriptPath()
            _workspace = os.path.join(_root,'workspace')
            _lib_path = os.path.join(_workspace,'libs')
             
            if not unzipFile(_root + os.sep + 'workspace.zip', _root+os.sep+'workspace'):
                log.fdbg('Unzip "workspace.zip" failed.')
                break
            
            _lib_names = []
            _str_libs = ''
            for _lib_name in os.listdir(_lib_path):
                _lib_names.append(_lib_path + os.sep + _lib_name)
            _str_libs += ';'.join(_lib_names)                
            log.fdbg('Libraries need to import = ' + _str_libs)
            
            _job_configs = []
            for _cfg_file in _cfg_files:
                _real_file_path = _workspace + os.sep + _cfg_file
                if not os.path.exists(_real_file_path):
                    log.fdbg('the local job config file in command line is not exist: "%s"' % _real_file_path)
                    continue
                else:
                    _job_configs.append(_real_file_path)
    
            for _job_config in _job_configs:
                log.fdbg('Run local job from "%s" ' % _job_config)
                '''
                java -cp "C:\Users\Administrator\magicboat;C:\Program Files\Cisco Webex\MagicBoat\SDK\Java\MagicBoatSDK.jar" 
                    mbjob 
                    "C:\Users\Administrator\magicboat\workspace\DS_Sharing-20151216143001.xml" 
                    "C:\Users\Administrator\magicboat\workspace\libs\Windows_AutoIt_Native_TrainClient.zip;C:\Users\Administrator\magicboat\workspace\libs\Windows_Java_TASS_V1.jar;C:\Users\Administrator\magicboat\workspace\libs\Windows_Python_TrainPage.zip" 
                    3600000 
                    "C:\Users\Administrator\magicboat\abcdefg.log"
                '''
                
                EXEC_CMD(r'javaw -cp "%s;%s" %s "%s" "%s" "%s"' % (_root, MAGICBOAT_SDK, MAGICBOAT_JOB_LAUNCHER_NAME, _job_config, _str_libs, _bridge_log_file))
                _report_file = _workspace + os.sep + os.path.splitext(os.path.basename(_job_config))[0] + ".zip"
                if os.path.exists(_report_file):
                    log.fdbg('Copy report to jenkins server(%s:%s).' % (_jenkins_ip , _report_folder))
                    STAFCopyToRemoteMachine(_report_file, _jenkins_ip , _report_folder)
                else:
                    log.fdbg('No report file exist, if you job executed successfully, please make sure job launched as expected and "java[w].exe" for API job not be closed unexpected.')