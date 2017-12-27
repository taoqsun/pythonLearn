''' zip functions
'''
import os
from zipfile import ZipFile,ZIP_DEFLATED
import subprocess


def unzipFile(srcZipFile,dest_folder):
    _is_success = True
    if not os.path.isfile(srcZipFile):
        return False   
    zf = None
    try: 
        zf = ZipFile(srcZipFile)
        NameList = zf.namelist();
        for nameItem in NameList:
            zf.extract(nameItem,dest_folder)
        _is_success = True
    except Exception as e:
        print 'unzip from "%s" to "%s" failed with error: %s' % (srcZipFile,dest_folder,str(e))
    finally:
        if None != zf:
            zf.close()
        
    return _is_success
    
def _addToZip(zf, path, zippath):
    if not isinstance(zf,ZipFile):
        print "first parameter is not a zipfile object"
        return False
    if os.path.isfile(path):
        zf.write(path, zippath, ZIP_DEFLATED)
    elif os.path.isdir(path):
        zf.write(path,zippath)
        for nm in os.listdir(path):
            _addToZip(zf,os.path.join(path, nm), os.path.join(zippath, nm))

    return True

def zipToFile(srcDir, zipName):
    if not os.path.isdir(srcDir):
        return False
    if os.path.exists(zipName):
        os.remove(zipName)
        
#     log.dbg( 'zip "' + srcDir + '" to "' + zipName + '"')
    zf = ZipFile(zipName,'w',allowZip64=True)
    for fitem in os.listdir(srcDir):
        subfolder = os.path.join(srcDir,fitem)
        _addToZip(zf,subfolder,os.path.basename(subfolder))
    zf.close()
#     log.dbg( 'zip "%s" Done .'  % srcDir)
    return True

def unzipFileForMacOSX(srcDir,desDir):
    unzipResult = False
    unzipProcess = subprocess.Popen(('unzip -q ' + srcDir + ' -d ' + desDir),shell = True)
    returnValue = unzipProcess.wait()
    if returnValue == 0:
        unzipResult = True
    return unzipResult

