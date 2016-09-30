'''
Created on Sep 29, 2016

@author: sky
'''
import urllib2
from HTMLParser import HTMLParser


class PyHttpFileParser(HTMLParser):
    '''sub class of HTMLParser to query latest packge from build farm server
    '''


    
    def __init__(self, _url, _keyword):
        HTMLParser.__init__(self)
        self._rootURL = _url
        self._fileNameparttern = _keyword
        self._matchFiles = []
        self.links = []
    
    def Parse(self):
        '''implement to get the source of html and feed to htmlparser
        @return: nothing
        @rtype: nothing
        '''
        try:
            u = urllib2.urlopen(self._rootURL)
        except urllib2.URLError:
            print "The URL you provide is not accessible, please double check! (%s)" % self._rootURL
            return
        self.feed(u.read())
    
    def handle_startag(self, tag, attrs):
        if tag == "td" or tag == "a":
            attrs = dict(attrs)   # save us from iterating over the attrs
        if tag == "td" and attrs.get("class", "") == "title":
            self.extracting = True
        elif tag == "a" and "href" in attrs and self.extracting:
            self.links.append(attrs["href"])
                
    def handle_data(self,data):
        '''override method from super class to process data in parse process and store them when saticify customized condition
        @param data: pared data in this iterte
        @type characters: string
        @return: nothing
        @rtype: nothing
        '''
        strData = str(data)
        if strData.find( self._fileNameparttern ) >= 0 :
#             self.handle_startag('a','href="' + strData.replace('/','')+'"')
            self._matchFiles.append(strData.replace('/',''))#

    def handle_endtag(self, tag):
        if tag == "td":
            self.extracting = False

    def getLatestItem(self):
        '''latest data item machied the condition
        @return: the latest data item machied the condition in 'handle_data()' call
        @rtype: string
        '''
        llen = len(self._matchFiles)
        print 'self.links === ',self.links
        if llen > 0:
            return self._matchFiles[llen-1]

        return ""
oParser = PyHttpFileParser('http://tanfs.eng.webex.com/spare/share/clientta/ComponentFile_Pipeline/webex-windows-plugin/release/', 'atinst.exe')
# oParser = PyHttpFileParser('http://code-maven.com/print-html-links-using-python-htmlparser', 'atinst.exe')
oParser.Parse()
print  oParser.getLatestItem()