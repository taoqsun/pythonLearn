'''
Created on Nov 5, 2015

@author: Administrator
'''
windowsList=[0,1,2,3,4,5]
getBrowserPID=["1","2",""]
print filter(None, getBrowserPID)

print [x+x for x in windowsList if x%2 == 0]#[output expression  | iterator | optional parameter]

print [windowsList[x] for x in range(len(windowsList))]