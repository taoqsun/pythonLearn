'''
Created on Oct 29, 2015

@author: sky
'''
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk(r'\\10.224.84.5\ta.vscmta.ta\ComponentFile_Pipeline\webex-windows-plugin\release'):
    f.extend(filenames)
    break
print f