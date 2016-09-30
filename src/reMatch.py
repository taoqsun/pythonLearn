# -*- coding: utf-8 -*-
import copy
import re

a = [[1],[2],[3]]
b = copy.copy(a)

print "before", "=>"
print a
print b

# modify original
a[0][0] = 0
a[1] = None

print "after", "=>"
print a
print b

print "this is RE match...."
strList = ["ad","kkk","cc"]
strLL = 'd|c'
print re.escape(strLL)
for itemTemp in strList:
#     print re.search(strLL,itemTemp)
    if re.search(strLL,itemTemp):
        print itemTemp