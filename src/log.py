import sys
import time
import os

def _3ItemsOperator(condition, success_ret, fail_ret):
    if (condition):
        return success_ret
    else:
        return fail_ret

def castStringToBool(str_bool_value):
    bool_str = str(str_bool_value.lower().strip())
    if bool_str not in ('false','true'):
            return False
    
    if 'false' == bool_str:
        return False
    else:
        return True

        
def getCurrentScriptPath(): 
    try:   
        _cur_file = __file__
    except Exception:
        _cur_file = sys.path[0]
        
    return os.path.dirname(os.path.realpath(_cur_file))

class Logger():
    def __init__(self, log_file_path = ''):
        self.__fhandle = None
        self.__cache = []
        self.__isWriting = False
        try:
            if not os.path.exists(log_file_path):  
                print 'Logger: file path not exist "%s" , create log directory at' % log_file_path
                os.makedirs(log_file_path)
            self.__logFile = log_file_path + os.sep + os.path.basename(__file__) + "-%s.log" % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
#             print self.__logFile
            self.__fhandle = open(self.__logFile,"wb")
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
               
    def fdbg2(self,log_str,msg_type = 'I',output_to_stdout = True):
        str_msg = self.__construct_output_msg(log_str, msg_type)
        if self.__isWriting:
            print 'caching...'
            self.__cache.append(str_msg)
        else:
            self.__isWriting = True
            for _item in self.__cache:
                if output_to_stdout == True:
                    sys.stdout.writelines(str_msg + os.linesep)                       
                if self.__fhandle!=None:
                    self.__fhandle.writelines(str_msg + os.linesep)
                    self.__fhandle.flush()
            self.__isWriting = False   


# log = Logger(getCurrentScriptPath())
print 4/2*2

