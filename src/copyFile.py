'''
Created on Aug 19, 2016

@author: sky
'''
import os
import shutil
import types
from _ast import TryExcept

def scanFileInFolder(folder, extension, excludes, include_sub_folder):
#     print 'in scanfiles in folder %s, %s ,%s, %s' % (folder,extension,excludes,include_sub_folder)
    _ret = []
    if not os.path.exists(folder):
        print 'Folder for scan not exist(%s)' % folder
        return _ret
    
    if (None !=excludes and not isinstance(excludes,types.TupleType)):
        return _ret
    
    fItems =  os.walk(folder)
    for _rootdir,_folders,_files in fItems:
        for _file in _files:
            _real_fItem = os.path.join(_rootdir, _file)
            if '' != extension and os.path.splitext(_real_fItem)[1].lower().strip() != extension.lower().strip():
                continue
            b_contain_exclude_str = False
            if None != excludes:
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

def copyFiles(srcDir,dstDir,extension, excludes,include_sub_folder):
    try:
        if os.path.isdir(srcDir) and os.path.isdir(dstDir):
            wantToCopyFilesList = []
            wantToCopyFilesList = scanFileInFolder(srcDir,extension, excludes,include_sub_folder)
            if not os.path.exists(dstDir):
                os.makedirs(dstDir, mode=0777)
            if len(wantToCopyFilesList) != 0: 
                for wantTofCopyFile in wantToCopyFilesList:
                    shutil.copy2(wantTofCopyFile,dstDir)
            else:
                print "nothing to copy ..."
        
        elif os.path.isfile(srcDir) and os.path.isfile(dstDir):
            shutil.copy2(srcDir,dstDir) 
        
        elif os.path.isfile(srcDir) and os.path.isdir(dstDir):
            if not os.path.exists(dstDir):
                os.makedirs(dstDir, mode=0777)
            shutil.copy2(srcDir,dstDir)
        else:
            print "%s,%s is useless" % (srcDir,dstDir)
    except Exception,e:
        print "copy %s to %s failed ,error message %s:" %(srcDir,dstDir,str(e))

def copyFile(srcFile,dstDir,overwrite):
    try:
        if not os.path.isfile(srcFile) :
            log.fdbg( "copy file failed,%s is not a file."% srcFile)
            return False
        elif srcFile == dstDir :
            return True
        if os.path.isdir(dstDir) :
            dstFile = os.path.join(dstDir,os.path.basename(srcFile))
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
        log.fdbg(  "copy %s to %s failed ,error message %s:" %(srcFile,dstDir,str(e)))
        return False
    return True        
print copyFile("/Users/sky/Desktop/1.txt", "/tmp", True)
print os.path.isfile("/tmp/2.txt")