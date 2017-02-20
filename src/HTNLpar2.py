'''
Created on Sep 30, 2016

@author: sky
'''
import HTMLParser
import urllib
class parseLinks(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag =='a':
            for name,value in attrs:
                if name =='href':
                    print value
                    print self.get_starttag_text()
lParser = parseLinks()
lParser.feed(urllib.urlopen("http://tanfs.eng.webex.com/spare/share/clientta/ComponentFile_Pipeline/webex-windows-plugin/release/").read())

strT = 'ii.pyy'
print strT[:-4]