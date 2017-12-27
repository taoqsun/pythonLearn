import os
import sys
import subprocess as _subprocess
import threading
from xml.dom import minidom,Node
import types
from operator import isCallable

from cilogger import createLogger
log = createLogger()


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

def getCurrentScriptPath(is_main_module = True): 
    _cur_file = ''
    if not is_main_module:
        try:   
            _cur_file = __file__
        except Exception:
            pass
    else:
        _cur_file = sys.argv[0]
        
    return os.path.dirname(os.path.realpath(_cur_file))

'''Ip functions
'''
import socket
   
def getHostIPAdress():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        port
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1" 

def iswindows():
    if os.name.startswith('nt'):
        return True
    
    return False

def ismacosx():
    if os.name.startswith('posix') and sys.platform.startswith('darwin'):
        return True
    
    return False

def islinux():
    if os.name.startswith('posix') and sys.platform.startswith('linux'):
        return True
    
    return False

def addenv(varname,newvalue):
    try:
        temp = os.environ[varname] + ';'
    except Exception,e:
        temp = ''
        log.dbgInfo(str(e))
    finally:
        os.environ[varname] = temp + newvalue

def constructHttpsUrl(site_url):
    if -1 == site_url.find('http'):
        _strHttps = 'https://' + site_url
    elif -1 == site_url.find('https'):
        _strHttps = site_url.replace('http','https')
    else:
        _strHttps = site_url

    return _strHttps 

#https://docs.python.org/2/library/subprocess.html#module-subprocess
class TimeoutExpired(Exception):
    def __init__(self, cmd, timeout, output=None):
        self.cmd = cmd
        self.timeout = timeout
        self.output = output

    def __str__(self):
        return ("Command '%s' timed out after %s seconds" %  (self.cmd, self.timeout))
        
def EXEC_CMD(cmd, search_in_output_str = '', search_founded_return = False, output_list = None,timeout = 300):
    '''execute a shell command
    @param search_in_output_str: the strings need to search from output, default is empty string
    @type characters: string
    @param search_founded_return: the result need to return when 'search_in_output_str' founded in output string, default False
    @type characters: boolean
    @param output_list: output buffer of running command
    @type characters: list
    @param timeout: timeout value of current command can continue, in second
    @type timeout: integer
    @return: result of the command, when 'search_in_output_str' is not empty, it is rely on 'search_founded_return'
    @rtype: boolean
    '''
    bSuccess = False
    try:
        def _exec_thread(subpobj, out_putlist):
            (_stdoutdata, _stderrdata) = subpobj.communicate(None) 
            out_putlist.append(_stdoutdata)
                
        ret = 0
        _output = []  
        p = _subprocess.Popen(cmd, bufsize = -1,shell=True,stdout=_subprocess.PIPE, stderr = _subprocess.PIPE)
        thread = threading.Thread(target=_exec_thread, args=(p, _output))
        thread.start()        
        thread.join(timeout)
        ret = p.returncode
        if thread.is_alive():
            p.terminate()
            thread.join()            
            raise TimeoutExpired(cmd, timeout)
        else:
            if '' == search_in_output_str or None == search_in_output_str:
                bSuccess = True
            else:           
                bSuccess = _3ItemsOperator( -1 != _output[0].find(search_in_output_str), search_founded_return,not search_founded_return )  
            if None != output_list and isinstance(output_list,types.ListType):
                del output_list[:]
                output_list.append(_output[0].strip())
    except Exception,e:
        if None != output_list and isinstance(output_list,types.ListType):
            del output_list[:]
            output_list.append( 'EXEC_CMD(%s) \r\n\t Exception: %s' % (cmd,str(e).strip()) )
        
    return bSuccess

def getValuesByTagName(xml_node, tagName, default_type = str ,default_value = ''):
    _type_callable = isCallable(default_type)
    valuelist = []
    taglist = xml_node.getElementsByTagName(tagName)
    if 0 != len(taglist):
        for tagNode in taglist:
            if None != tagNode.firstChild:
                if _type_callable:
                    valuelist.append(default_type(tagNode.firstChild.nodeValue))
                else:
                    valuelist.append(tagNode.firstChild.nodeValue)
    else:      
        if _type_callable:
            valuelist.append(default_type(default_value))
        else:
            valuelist.append(default_value)

    return valuelist
 
def getChildrenByTagName(parent_node,tag_name):
    if not isinstance(parent_node,Node) or not isinstance(tag_name, types.StringTypes):
        return []
    
    return parent_node.getElementsByTagName(tag_name)