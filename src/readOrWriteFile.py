'''
Created on Dec 11, 2015

@author: Administrator
'''
import os

def readOrWriteMeetingCountFile(meetingCount,isRead = True):
    file_handle=None
    filePath = os.path.dirname(os.path.abspath(__file__))
    fileName=filePath + os.sep +'meetingCount.ini'
    if not isRead:
        try:         
            file_handle = open(fileName,"w")
            file_handle.writelines(meetingCount)
        except:
            return False
        finally:
            file_handle.close()
    else:
        leaveCount = ''
        try:         
            file_handle = open(fileName,"r")
            leaveCount = file_handle.readline()
        except:
            return False
        finally:
            file_handle.close()
        return int(leaveCount)

if __name__ == '__main__':
    caseNumber = 10
    n = 0
    for case in range(caseNumber):
        meeting_count = 10 
        if os.path.isfile(r'C:\meetingCount.ini'):
            realCount = readOrWriteMeetingCountFile(0, True) - 1 
            readOrWriteMeetingCountFile(str(realCount), False)        
        else:
            if None != meeting_count:
                realCount = int(meeting_count) - 1
                readOrWriteMeetingCountFile(str(realCount), False)
            else:
                print "meeting count is none"
                realCount = 0
        
        if 0 < realCount :
            n = n + 1
            print "shut down",n
        else:
            n = n + 1
            print "delete file ===",n
            os.remove(r'C:\meetingCount.ini')