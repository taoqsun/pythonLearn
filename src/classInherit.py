'''
Created on Feb 16, 2017

@author: sky
'''
class cls1():
    def __init__(self):
        self._variableName = "11"
    def setValue(self,values):
        self._variableName = values
        
class cls2(cls1):
    def __init__(self):
        cls1.__init__(self)
        
    def test(self):
        c1 = cls1()
        c1.setValue("22")
        print c1._variableName
        print self._variableName
class2 = cls2()
class2.test()