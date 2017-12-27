'''shell functions
'''
import os
import sys
import shutil
import types
import stat

from ciutil import iswindows,islinux,ismacosx,EXEC_CMD
from cierror import *

from cilogger import createLogger

log = createLogger()

def copyFile(srcFile,dstDir,overwrite = True):
    try:
        if not os.path.isfile(srcFile) :
            log.fdbg( "copy file failed,%s is not a file."% srcFile,'E')
            return False
        elif os.path.abspath(srcFile) == os.path.abspath(dstDir) :
            return True
        if os.path.isdir(dstDir) :
            dstFile = os.path.join(dstDir,os.path.basename(srcFile))
            if os.path.abspath(srcFile) == os.path.abspath(dstFile) :
                return True
            if os.path.exists(dstFile):
                if  overwrite:
                    os.remove(dstFile)
                else:
                    return False
            dstDir = dstFile
        elif os.path.isfile(dstDir) :
            if  overwrite:
                os.remove(dstDir)
            else:
                return False
        shutil.copyfile(srcFile, dstDir)
    except Exception,e:
        log.fdbg(  "copy %s to %s failed ,error message %s:" %(srcFile,dstDir,str(e)),'E')
        return False
    return True 

def copyTree(src, dst, ignore_exts = () ,symlinks = False, ignore = None):
    try:
        if not os.path.exists(dst):
            os.makedirs(dst)
            shutil.copystat(src, dst)
        lst = os.listdir(src)
        if ignore:
            excl = ignore(src, lst)
            lst = [x for x in lst if x not in excl]
        for item in lst:
            if os.path.splitext(item)[1] in ignore_exts:
                continue
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)
                os.symlink(os.readlink(s), d)
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)
                except:
                    pass # lchmod not available
            elif os.path.isdir(s):
                copyTree(s, d, ignore_exts, symlinks, ignore)
            else:
                shutil.copy2(s, d)
        return True
    except Exception as e:
        log.fdbg('copy directory from (%s) to (%s) failed: %s' % (src,dst, str(e)),'E')
    
    return False
  
DELETE_FILE = 0X0002
DELETE_DIR = 0X0004
DELETE_ALL = 0X0006

def deleteItemsInDirectory(target_dir, option = DELETE_ALL, excludeNameList = (),del_root_dir = False): 
    if not os.path.exists(target_dir):
        log.dbg(target_dir + ' not exist')
        return ERROR_FILE_NOT_FOUND
    try:
        log.fdbg('Trying to delete "%s"' % target_dir)
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
        return ERROR_IO_EXCEPTION

    return ALL_SUCCESS

def modifyLinuxFolderToWrite( folder):
    try:
        if islinux():
            os.popen('chmod 777 -Rf %s' % folder)
        elif ismacosx():
            os.popen('chmod -Rf 777 "%s"' % folder)
    except Exception,e:
        log.fdbg('chmod 777 ,exception message :' +str(e))  
        
def createMultiLevelDirectory(parent_folder, sub_folder_names, remove_existing = True, add_rw_permission = True): 
    if  '' == str(sub_folder_names.strip()):
        log.fdbg('sub folder names empty when trying to create multiple level directories %s', 'E', True)
        return ERROR_INVALID_PARAMETER

    if None == parent_folder or '' == parent_folder :
        parent_folder = ''
    elif not os.path.exists(parent_folder):
        log.fdbg( 'Create folder, parent not exist(%s),(%s)' % (parent_folder, str(sub_folder_names)))
        return ERROR_FILE_NOT_FOUND
    
    if iswindows():
        _replace_sep = '/'
    else:
        _replace_sep = '\\'
    _os_sub_folder = sub_folder_names.replace(_replace_sep, os.sep).strip()
    
    try:
        _last_child_path = os.path.join(parent_folder, _os_sub_folder)
        if os.path.exists(_last_child_path):
            if remove_existing:
                shutil.rmtree(_last_child_path)
            else:
                return ALL_SUCCESS
        
        if isinstance(add_rw_permission, types.BooleanType) and add_rw_permission:
            os.makedirs(_last_child_path)
        else:
            os.makedirs(_last_child_path,0755)
            
    except Exception,e:
        log.fdbg( 'create directory exception with message: %s' % str(e),'E')
        return ERROR_IO_EXCEPTION
    
    return ALL_SUCCESS

def scanFileInFolder(folder, extensions, excludes, include_sub_folder):
#     print 'in scanfiles in folder %s, %s ,%s, %s' % (folder,extensions,excludes,include_sub_folder)
    _ret = []
    if not isinstance(extensions, types.TupleType) or not isinstance(excludes, types.TupleType):
        log.fdbg('Invalid extension or excludes value data type.')
        return _ret
    
    if not os.path.exists(folder):
        log.fdbg('Folder for scan not exist(%s)' % folder)
        return _ret
    
    fItems =  os.walk(folder)
    for _rootdir,_folders,_files in fItems:
        for _file in _files:
            _real_fItem = os.path.join(_rootdir, _file)
            if '*' not in extensions and not os.path.splitext(_real_fItem)[1].lower().strip() in extensions:
                continue
            b_contain_exclude_str = False            
            for _exclude_item in excludes:
                if '' != _exclude_item and -1 != _file.find (_exclude_item) :# if file name contain excluded string
                    b_contain_exclude_str = True
                    break
            if b_contain_exclude_str:
                continue
            _ret.append( _real_fItem )
        if not include_sub_folder:
            break
        
    return _ret

import datetime

def cleanHistories(root_dir, extensions = ('*',), days_to_keep = 7, excludes = (), include_sub_dir = True):
#     print root_dir, extensions, days_to_keep, excludes,include_sub_dir
    if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        log.fdbg('the folder not exist or not a directory(%s), nothing to do.' % root_dir)
        return True
    
    if not isinstance(extensions, types.TupleType) or not isinstance(days_to_keep, types.IntType) \
        or not isinstance(excludes, types.TupleType) or not isinstance(include_sub_dir, types.BooleanType):
        log.fdbg('cleanHistories() invalid parameters "%s, %s, %d, %s, %s"' % (root_dir,str(extensions),days_to_keep,str(excludes),str(include_sub_dir)))
        return False
    
    if 0 ==len(extensions):
        return False
    
    #_check_all_items = 
    #_cur_tm = time.localtime(time.time())
    for _fItem in os.listdir(root_dir): 
        _abs_fItem = os.path.join(root_dir,_fItem)       
        if not ('*' in extensions) and os.path.isfile(_abs_fItem) \
                and os.path.splitext(_fItem)[1].lower().strip() not in extensions:
            continue
        
        b_contain_exclude_str = False
        for _exclude_item in excludes:
            if -1 != _fItem.find (_exclude_item) :
                b_contain_exclude_str = True
                break
            
        if b_contain_exclude_str or not os.path.exists(_abs_fItem):
            continue

        _f_dt = datetime.datetime.fromtimestamp(os.path.getmtime(_abs_fItem))
        _dt_offset = datetime.timedelta(days = abs(days_to_keep))
        _dt_now = datetime.datetime.now()
        try:
            if os.path.isdir(_abs_fItem) and include_sub_dir :
                cleanHistories(_abs_fItem, extensions, days_to_keep, excludes, include_sub_dir)
                if os.path.exists(_abs_fItem) and 0 == len(os.listdir(_abs_fItem)) and (_dt_now - _dt_offset) > _f_dt:
                    log.fdbg('Remove empty folder %s' % _abs_fItem)
                    os.rmdir(_abs_fItem)
            elif os.path.isfile(_abs_fItem) and (_dt_now - _dt_offset) > _f_dt:
                log.fdbg('Remove: %s' % _abs_fItem)
                os.remove(_abs_fItem)
                _parent_fold = os.path.dirname(_abs_fItem)
                if 0 == len(os.listdir(_parent_fold)):
                    log.fdbg('Delete the empty directory %s.' % _parent_fold)
                    os.rmdir(_parent_fold)
                    
        except Exception,e:
            log.fdbg('clean history exception: %s, ignore' % str(e),'E')
           
    return True
           
'''
@author yifhu
'''
#get modify interval until current time
def getModifyInterval(path):
    statInfo=os.stat(path)
    timeInterval=time.time()-statInfo.st_mtime
    return timeInterval

# para modiTime: modify time interval ;setIntervalTime(seconds): set interval time to define if  Git pull change local files
# return true:modified ;false:not modified
def hasFileChange(root_dir,setIntervalTime):
    _l_file_modify=[]
    for parent,dirnames,filenames in os.walk(root_dir):    
        for filename in filenames:
            if len(_l_file_modify) > 1000:
                log.fdbg('There are too much files in searching tree, aborted.') 
                return True
            else:                 
                _l_file_modify.append(getModifyInterval(os.path.join(parent,filename)))
    _l_file_modify.sort(cmp=None, key=None, reverse=False)
    
    modiTime= _l_file_modify[0]
    if modiTime < setIntervalTime:
        return True
    else:
        return False

def mountFolderToLocal(localFolderDir,remoteAddress,realDir,virtualDir,domain = '',account = '',password = ''):
    mountReturnResult = False
    remoteDir = ""
    mountCMD = ""
    if localFolderDir == "" or remoteAddress == ""  :
        log.fdbg("mountFolderToLocal : localFolderDir or remoteAddress is null ...")
        return mountReturnResult    
    
    if not os.path.isdir(localFolderDir) and not iswindows():
        try:
            os.makedirs(localFolderDir)
        except Exception,e:
            log.fdbg("mountFolderToLocal : create localFolderDir failed ...")
            return mountReturnResult
    else:
        if os.path.ismount(localFolderDir):
            log.fdbg('The path has also been mounted, but can not check the mount source')
            return True
        elif os.path.exists(localFolderDir) and len(os.listdir(localFolderDir)) > 0:
            log.fdbg('warning: the local mount point is in-use...')
            #return False
    try:
        if islinux() :
            realDir = realDir.replace("\\",os.sep)
            if realDir == "" :
                log.fdbg("mountFolderToLocal : realDir is null ...")
                return mountReturnResult                
#             mount -t nfs qanfs.qa.webex.com:/spare/share /User/sky/tmp
            #remoteDir = os.path.join(remoteAddress + ":",realDir)
            mountCMD = 'mount -t nfs %s %s' % ("%s:%s"%(remoteAddress,realDir),localFolderDir)
        elif ismacosx() :
            
            realDir = realDir.replace("\\",os.sep)
            virtualDir = virtualDir.replace("\\",os.sep)
            if virtualDir == "" :
                log.fdbg("mountFolderToLocal : virtualDir is null ...")
                return mountReturnResult
            if domain != "" and account != "" and password != "" :
#              mount_smbfs //test:pass@qanfs.qa.webex.com/public /User/sky/tmp
#              mount_smbfs '//CCTG-TA-CIFS-1;smb4mac:wbxAaR00t@10.194.246.26/vol_ta_data/spare/share//' /Volumes/CLIENTTA_LOGS
                remoteDir = "'//" + domain +';' + account + ':' + password + '@' + "%s%s"%(remoteAddress,realDir) +"//'"
                mountCMD = 'mount_smbfs %s %s' % (remoteDir,localFolderDir)
            elif account != "" and password != "" and domain == "":
                remoteDir = "//" + account + ':' +password + '@' + "%s%s"%(remoteAddress,virtualDir)
                mountCMD = 'mount_smbfs %s %s' % (remoteDir,localFolderDir)
            else:
#              mount_smbfs //test@qanfs.qa.webex.com/public /User/sky/tmp
                remoteDir = '//' + account +'@' + "%s%s"%(remoteAddress,virtualDir)
                mountCMD = 'mount_smbfs %s %s' % (remoteDir,localFolderDir)
        elif iswindows() :
            
            realDir = realDir.replace("/",os.sep)
            virtualDir = virtualDir.replace("/",os.sep)
            if virtualDir == "" :
                log.fdbg("mountFolderToLocal : virtualDir is null ...")
                return mountReturnResult
            remoteDir = '\\\\' + "%s%s"%(remoteAddress,virtualDir)
            if domain == "" and account != "" and password != "":
#              net use F: \\qanfs.qa.webex.com\public pass /user:test
                mountCMD = 'net use %s %s %s /user:%s' % (localFolderDir,remoteDir,'"'+password+'"','"'+account+'"')
            elif domain != "" and account != "" and password != "":
#                 net use F: \\tanfs.eng.webex.com\vol_ta_data "password" /USER:"CCTG-TA-CIFS-1\wbxroot"
                mountCMD = 'net use %s %s %s /user:%s' % (localFolderDir,remoteDir,'"'+ password+'"','"'+ domain + '\\' + account+'"')
            else:
#              net use F: \\qanfs.qa.webex.com\public 
                mountCMD = 'net use %s %s' % (localFolderDir,remoteDir)
        else:
            log.fdbg("mountFolderToLocal : unknow OS...")
            return mountReturnResult
        log.fdbg("mountFolderToLocal : command line = %s" % mountCMD)
        EXEC_CMD(mountCMD)
    except Exception,e:
        log.fdbg('mount %s to local: %s, exception message: %s' % (remoteDir,localFolderDir,str(e)))
    if iswindows():
        if os.path.isdir(localFolderDir):
            mountReturnResult = True
    else:
        if os.path.ismount(localFolderDir):
            mountReturnResult = True
    return mountReturnResult
