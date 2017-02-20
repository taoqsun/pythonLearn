'''
Created on Mar 15, 2016

@author: Administrator
'''
listTemp = ["1","2"]
listTemp2 = []
print listTemp2
#print "".join(filter( None,listTemp)) == ""
print listTemp
dictTemp = {"ee":1}
if dictTemp.has_key("aa"):
    dictTemp["aa"]
listTemp2.insert(0, "object")  
listTemp2.extend(listTemp)
print listTemp2
print "_".join(listTemp2)
component_names_list = "1,2,3"
print component_names_list.split(";")

tempDict = {"1":1,"2":2}
tempDict2 = {"2":2,"3":3}
print tempDict,tempDict2
for tempk in tempDict.keys():
    if tempDict2.has_key(tempk):
        tempDict[tempk] = tempDict2[tempk]
        del tempDict2[tempk]
print tempDict,tempDict2
tempDict.update(tempDict2)
print tempDict,tempDict2