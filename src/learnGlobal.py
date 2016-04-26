'''
Created on Apr 25, 2016

@author: Administrator
'''


global globalPara2

def cc():
    print " cc =",globalPara2

if __name__ == "__main__":
    
    globalPara = "1"
#     cc()
    globalPara2 = globalPara + " 333"
#     cc()
    print globalPara2
    globalPara2 = " 444 "
    cc()