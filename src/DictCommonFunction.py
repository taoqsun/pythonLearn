'''
Created on Sep 5, 2016

@author: sky
'''
tempDict = {1:"1"}
print "tempDict =",tempDict
# print tempDict(0)
# for keydd in tempDict.keys():
#     if keydd == 1:
#         del tempDict[keydd]
# print tempDict
projectInfo_dict = {2:"2",1:"3"}
print "projectInfo_dict =" ,projectInfo_dict
# if not isinstance(projectInfo_dict, types.DictionaryType):return False
for project_key in projectInfo_dict.keys():
    if tempDict.has_key(project_key):
        tempDict[project_key] = projectInfo_dict[project_key]
        del projectInfo_dict[project_key]
tempDict.update(projectInfo_dict)
print "tempDict =",tempDict
print "projectInfo_dict =",projectInfo_dict
