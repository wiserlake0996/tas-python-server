import time

class CusTimer(object):
    def __init__(self):
        self.currentTime = 0
        
    def getTime(self):
        return time.time()
        
    def checkTime(self, old, new):
        if (new - old) >= 60:
            return True
        return False
        
t = CusTimer()
print t.getTime();

print t.checkTime(322,24)

    