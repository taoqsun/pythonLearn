'''
Created on Oct 15, 2015

@author: sky
'''
# import os
# def tree(top):
#     for path, names, fnames in os.walk(top):
#         for fname in fnames:
#             yield os.path.join(path, fname)
#   
# for name in tree('C:\Users\XXX\Downloads\Test'):
#     print name
    
# alist = ['a1', 'a2', 'a3']
# blist = ['1', '2', '3']
#  
# for a, b in zip(alist, blist):
#     print a, b


# class decorator(object):
#  
#     def __init__(self, f):
#         print("inside decorator.__init__()")
#         f() 
# # Prove that function definition has completed
#  
#     def __call__(self):
#         print("inside decorator.__call__()")
#  
# @decorator
# def function():
#     print("inside function()")
#  
# print("Finished decorating function()")
#  
# function()

# def decorator(func):
#     def modify(*args, **kwargs):
#         variable = kwargs.pop('variable', None)
#         print variable
#         x,y=func(*args, **kwargs)
#         return x,y
#     return modify
#  
# @decorator
# def func(a,b):
#     print a**2,b**2
#     return a**2,b**2
#  
# func(a=4, b=5, variable="hi")
# func(a=4, b=5)
 
# hi
# 16 25
# None
# 16 25