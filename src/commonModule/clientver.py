# -*- coding:utf-8 -*-
"""
@desc:  retrieve client version(s) deployed on given test site(s)
"""
import os
import random 
import urllib2
from urllib2 import URLError
from threading import Thread
from cilogger import createLogger
from citypes import *
from ciutil import constructHttpsUrl
log = createLogger()

class clientVerParser(Thread): 
    RANDOM_SUFFIX = str(random.uniform(0,1))[2:]
    DEFAULT_VER_STR = 'WBXclient-UNKNOWN-%s' % RANDOM_SUFFIX

    def __init__(self,name=None,args=(),kwargs={}):
        Thread.__init__(self,None,None,name,args,kwargs)
        self._sites_info = args
        self._site_clientVer = {}
    
    def __getClientVersion(self,strDomainURL, strSiteName):
        """get build number about current client build
        """
        _subUrl = ''
        _mcRoot = ''
        _clientRoot = ''
        _bFoundMainFrame = False
        _strDomainURL = constructHttpsUrl(strDomainURL)
        try:
            oUrl = urllib2.urlopen(_strDomainURL +'/' + strSiteName + '/mc')       
            for line in oUrl:
                if (-1 == line.find('<FRAME SCROLLING="auto" NORESIZE NAME="mainFrame"')):
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
            
            _mcRoot =  os.path.dirname(_strDomainURL + _subUrl)
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
        except URLError, e:
            log.fdbg('__getClientVersion() exception: %s (%s)' % (str(e), _strDomainURL +'/' + strSiteName))
            return ''
        except ValueError,e:
            log.fdbg('__getClientVersion() exception: %s (%s)' % (str(e), _strDomainURL +'/' + strSiteName))
            return ''

        return  _strVersion
    
    def getVersions(self):
        return self._site_clientVer
    
    def getVersString(self,is_need_site_info = False):
        _ver_str = []
        for _site in self._site_clientVer:
            if is_need_site_info:
                _ver_str.append(self._site_clientVer[_site] + '(%s)' % _site)
            else:
                _ver_str.append(self._site_clientVer[_site])
                
        return ';'.join(_ver_str)
    
    @classmethod
    def getDefaultVerString(cls):
        return cls.DEFAULT_VER_STR
    
    def run(self):
#         log.fdbg('Starting to retrieve client version for configured test site(s)...' )
        if 0 == len(self._sites_info):
            log.fdbg('There is no site information given when try to retrieve client version(s).','W')
            self._site_clientVer['UNKNOWN'] = self.DEFAULT_VER_STR

        for _site_info in self._sites_info:
            if isinstance(_site_info, SiteInfo):
                _cur_site_urlname = '/'.join((_site_info.site_url, _site_info.site_name))
                if self._site_clientVer.get(_cur_site_urlname) != None:
                    continue
                _cur_ver_str = self.__getClientVersion(_site_info.site_url, _site_info.site_name)
#                 log.fdbg('Client Version of "%s/%s" is : %s' % (_site_info.site_url, _site_info.site_name, _cur_ver_str))
                if '' == _cur_ver_str:
                    self._site_clientVer[_cur_site_urlname] = self.DEFAULT_VER_STR
                else:
                    self._site_clientVer[_cur_site_urlname] = _cur_ver_str + '-%s' % clientVerParser.RANDOM_SUFFIX
            else:
                log.fdbg('the site information object is invalid.')

#         log.fdbg('Retrieve client version for configured test site(s) completed.')