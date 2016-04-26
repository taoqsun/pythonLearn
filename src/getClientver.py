'''
Created on Apr 22, 2016

@author: Administrator
'''
import os
from urllib2 import URLError
import sys
import urllib2
from collections import namedtuple
import random

CLIENT_VER_ENVPARAM = 'BUILD_VERSION'
CLIENT_VER_PROPFILE = 'clientver.properties'
#function/src/buildver.properties
#${BUILD_VERSION}

def getCurrentScriptPath():
    curPath = sys.path[0]
    if os.path.isfile(curPath):
        curPath = os.path.dirname(curPath)
    return curPath

def constructHttpsUrl(site_url):
    if -1 == site_url.find('http'):
        _strHttps = 'https://' + site_url
    elif -1 == site_url.find('https'):
        _strHttps = site_url.replace('http','https')
    else:
        _strHttps = site_url

    return _strHttps 

SiteInfo = namedtuple('SiteInfo', ['site_url','site_name','user_name','user_password'], rename = True)

class clientVerParser(): 
    def __init__(self,site_info=None,save_to=''):
        self._site_info = site_info
        self._site_clientVer = {} #{site_url-site_name:version string}
        self._save_to = save_to
    
    def __getClientVersion(self,strDomainURL, strSiteName):
        '''get build number about current client build
        '''
        _subUrl = ''
        _mcRoot = ''
        _clientRoot = ''
        _bFoundMainFrame = False
        _strDomainURL = constructHttpsUrl(strDomainURL)
        try:
            oUrl = urllib2.urlopen(_strDomainURL +'/' + strSiteName + '/mc')    #Raises URLError on errors.
            #isinstance(oUrl, types.FileType) return False
        except URLError, e:
            print str(e)
            return ''
    
        for line in oUrl:
            if (-1 == line.find('<FRAME SCROLLING="auto" NORESIZE NAME="mainFrame"') ):
                continue
            asubstr = line.split(' ')
            for attri in asubstr:
                if attri.find('=') == -1:
                    continue
                namevalue = attri.split('=')
                if namevalue[0].lower() != ('src'):
                    continue
                _subUrl = namevalue[1].replace('"','')
                _subUrl = _subUrl.replace('&#47;','/')
                _bFoundMainFrame = True
                break
            if _bFoundMainFrame:
                break
        oUrl.close()
        
        _mcRoot =  os.path.dirname(_strDomainURL + _subUrl)#https: //hjt31.qa.webex.com/mc3100/meetingcenter/support/support.do?siteurl=hjt31&Action=downloads  
        print " open url =" + _mcRoot + "/support/support.do?siteurl=" + strSiteName + "&Action=downloads"
        oUrl = urllib2.urlopen(_mcRoot + "/support/support.do?siteurl=" + strSiteName + "&Action=downloads")
        for line2 in oUrl:
            if (-1 == line2.find(_strDomainURL + '/client') ):
                continue       
            asubstr = line2.split('=')
            _clientRoot = os.path.dirname(asubstr[1].replace('"',''))
            break
        oUrl.close()
        oUrl = urllib2.urlopen(_clientRoot + "/version/verclient.txt")
        _strVersion = os.path.splitext(oUrl.read().strip())[0]
        oUrl.close()
        print 'Client Version of "%s/%s" is : %s' % (strDomainURL, strSiteName, _strVersion)
        return  _strVersion
       
    def go(self):
        print 'Starting to retrieve client version for configured test site(s)'
        _prop_file = os.path.join(getCurrentScriptPath(),CLIENT_VER_PROPFILE)
        if os.path.exists(_prop_file):
            os.remove(_prop_file)
        
        __fhandle = open(_prop_file,"wb")
        if None == __fhandle :
            return
        
        print 'Save client version information to "%s"' % _prop_file
        __vers = []
        
        if isinstance(self._site_info, SiteInfo):
            _cur_ver_str = self.__getClientVersion(self._site_info.site_url, self._site_info.site_name)
            if '' == _cur_ver_str:
                __vers.append('WBXclient-UNKNOWN-%s' % str(random.uniform(0,1))[2:7])
            else:
                __vers.append(_cur_ver_str + '%s' % str(random.uniform(0,1))[2:7])
        else:
            print 'the site information object is invalid.'
                
        __fhandle.writelines(CLIENT_VER_ENVPARAM + '=' + ';'.join(__vers))       
        __fhandle.close()


site_info = SiteInfo(site_url="atsclientta.webex.com",site_name="atsclientta",user_name='tauser',user_password='P@ss123')
# site_info = SiteInfo(site_url="t1wdta03.qa.webex.com",site_name="t1wdta03",user_name='tauser',user_password='P@ss123')
_prop_file = os.path.join(getCurrentScriptPath(),CLIENT_VER_PROPFILE)
clientver = clientVerParser(site_info,_prop_file)
clientver.go() 

