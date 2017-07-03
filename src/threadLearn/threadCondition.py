'''
Created on Apr 25, 2017

@author: Administrator
'''
#coding:utf8   
import  threading, time    
class  Hider(threading.Thread):    
    def  __init__( self , cond, name):    
        super(Hider,  self ).__init__()    
        self.cond = cond    
        self.name = name    
        
    def  run( self ):    
        time.sleep( 1 )    
            
        self.cond.acquire()  #b        

        self.cond.notify()  
        self.cond.wait()     
 
        self.cond.notify()
        self.cond.release()      

            
class  Seeker(threading.Thread):    
    def  __init__( self , cond, name):    
        super(Seeker,  self ).__init__()    
        self.cond = cond    
        self.name = name    
    def  run( self ):    
        self.cond.acquire()  

        self.cond.wait()    

#         print("\t[Info] {0} notify()...".format(self.name))  
        self.cond.notify()  
#         print("\t[Info] {0} wait()...".format(self.name))  
        self.cond.wait()
#         print("\t[Info] {0} release()...".format(self.name))  
        self.cond.release()     
 
            
cond = threading.Condition()    
seeker = Seeker(cond,  'seeker' )    
hider = Hider(cond,  'hider' )    
seeker.start()    
hider.start() 
