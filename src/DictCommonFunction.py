'''
Created on Sep 5, 2016

@author: sky
'''
tempDict = {1:"1"}
print tempDict
print tempDict(0)
for keydd in tempDict.keys():
    if keydd == 1:
        del tempDict[keydd]
print tempDict

