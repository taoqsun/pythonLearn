'''
Created on Feb 16, 2017

@author: sky
'''
from collections import namedtuple
SiteInfo = namedtuple('SiteInfo', ['site_url','site_name','user_name','user_password'])

_site_info = SiteInfo(site_url = "1",site_name= "2",
                                    user_name="3",
                                    user_password="4")
_site_info2 = SiteInfo(site_url = "1",site_name= "2",
                                    user_name="3",
                                    user_password="4")
_site_info3 = SiteInfo(site_url = "3",site_name= "2",
                                    user_name="3",
                                    user_password="4")
listDemo = []

listDemo.append(_site_info)
print listDemo
if _site_info2 not in listDemo:
    listDemo.append({1:0})
print listDemo
if{1:0} in listDemo:
    listDemo.remove({1:0})
print listDemo
listDemo.append(_site_info3)
for item in listDemo:
    print item