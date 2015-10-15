'''
Created on Sep 14, 2015

@author: sky
'''
import os

def GetProgramFiles32():
    if 'PROGRAMFILES(X86)' in os.environ :
        return os.environ['PROGRAMFILES(X86)']
    else:
        return os.environ['PROGRAMFILES']

def GetProgramFiles64():
    if 'PROGRAMFILES(X86)' in os.environ:
        return os.environ['PROGRAMW6432']
    else:
        return None
    
if __name__ == '__main__':
    print 'GetProgramFiles64()',GetProgramFiles64()
    print 'GetProgramFiles32()',GetProgramFiles32()