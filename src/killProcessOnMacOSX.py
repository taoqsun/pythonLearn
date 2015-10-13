'''
Created on Oct 13, 2015

@author: taoqsun
'''
import subprocess, signal
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
processName = "Meeting Center"
for line in out.splitlines():
#                     print line
    if processName in line:
        pid = int(line.split(None, 1)[0])
        os.kill(pid, signal.SIGKILL)