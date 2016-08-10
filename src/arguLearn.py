'''
Created on Apr 28, 2016

@author: Administrator
'''


import argparse
parser = argparse.ArgumentParser()
print 
parser.add_argument("-configFileName", dest = "configFileName" ,required=False, type=str, 
                    action="store", help = "the name of config file",default=None)
print parser
try:
    args = parser.parse_args()
except Exception,e:
    print "333 == ",e
# print args.configFileName
print "33"