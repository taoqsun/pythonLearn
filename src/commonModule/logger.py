'''

'''
import os
import sys
import time
from threading import Lock

class Logger():
    def __init__(self, log_file_name = '', log_file_path = ''):
        self.__fhandle = None
        self.__logFile = ''
        self.__flocker = Lock()
        self.__clocker = Lock()
        self._isconsoleapp = True
        if 'pythonw.exe' == os.path.basename(sys.executable).strip().lower():
            self._isconsoleapp = False
        try:
            _name_suffix = "-%s.log" % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            _log_file_path = log_file_path
            if '' == _log_file_path:
                _log_file_path = os.path.abspath(os.path.dirname(sys.argv[0]))
                
            if ''!=_log_file_path and (not os.path.isdir(_log_file_path) or not os.path.exists(_log_file_path)):  
#                 print 'Logger: Folder not exist "%s" , create log directory at' % _log_file_path
                os.makedirs(_log_file_path)
            if '' == log_file_name:
                self.__logFile = os.path.join(_log_file_path, os.path.basename(sys.argv[0]))  + _name_suffix
            else:
                self.__logFile = os.path.join(_log_file_path , log_file_name)  + _name_suffix
                    
        except Exception,eMsg:
            self.__logFile = os.path.join(_log_file_path, os.path.basename(sys.argv[0]))  + _name_suffix
#             print 'Logger Exception: "%s" ' % str(eMsg)
    
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
        if self.__clocker.acquire():
#             print self.__construct_output_msg(log_str, msg_type)  
            self.__clocker.release()
    
    def fdbg(self,log_str,msg_type = 'I',output_to_stdout = True):
        try:
            if self.__flocker.acquire():
                if None == self.__fhandle:
                    self.__fhandle = open(self.__logFile,"w")

                str_msg = self.__construct_output_msg(log_str, msg_type)
                if output_to_stdout == True and self._isconsoleapp:
                    sys.stdout.writelines(str_msg + os.linesep)                      
                if self.__fhandle!=None:
                    self.__fhandle.writelines(str_msg + os.linesep)
                    self.__fhandle.flush()
                    
                self.__flocker.release()
                
        except Exception,e:
#             print 'Exception in fdbg() call, error msg: %s' % str(e)
            self.__flocker.release()

g_log = None

def createLogger(log_path = ''):
    global g_log
    if None == g_log:
        if '' != log_path:
            g_log = Logger('', log_path)
        else:
            g_log = Logger('', os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])) , 'logs'))
    
    return g_log
