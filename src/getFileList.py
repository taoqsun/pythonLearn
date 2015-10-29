'''
Created on Oct 29, 2015

@author: sky
'''
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('mypath'):
    f.extend(filenames)
    break