#!/usr/bin/env python
#coding:utf-8

import fcntl
import os

class xLOCK:
    def __init__(self, name='/tmp/.raspx_cached/xLOCK.L'):
        self.flock = open(name, 'w')
        self.fid = self.flock.fileno()

    def lock(self):
        try:
            fcntl.lockf(self.fid, fcntl.LOCK_SH)
            # fcntl.lockf(self.fid, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except:
            return False

    def unlock(self):
        self.flock.close()

class xlog:
    def __init__(self,logfile):
        if not os.path.isfile(logfile):
            open(logfile,'w').close()
        self.logfile = logfile
        self.lock = xLOCK()

    def write(self,data):
        try:
            with open(self.logfile,'a+') as f:
                self.lock.lock()
                f.write(str(data))
                f.write('#^#')
                f.close()
                self.lock.unlock()
        except Exception as e:
            return e
        finally:
            self.lock.unlock()

    def read(self):
        with open(self.logfile, 'r') as f:
            tmp1 = f.read()
            f.close()
        data = []
        tmp2 = tmp1.split('#^#')
        for i in tmp2:
            if i != "":
                data.append(eval(i))
        return data


if __name__ == '__main__':
    data = {'fdsafds':43243243,"fdsafdsad":"004u3nujo32 43290uj432 ","fdsa":[12,321,32,13,12]}
    xg = xlog('/tmp/test.xlog')
    xg.write(data)
    a = xg.read()
    print a