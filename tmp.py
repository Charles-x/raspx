#!/usr/bin/env python
#coding:utf-8
from functools import wraps
# -1 = ready, 1 = using, 0 = error
lock_dic = { 'T_H':-1,'pinfo':-1,'pic':-1,'soil_H':-1,'irrigate': -1}

def xlock(lockname):
    def verify(func):
        @wraps(func)
        def verify_func(*args, **kwargs):
            global lock_dic
            if lock_dic[lockname] == -1:
                lock_dic[lockname] = 1
                try:
                    data = func(*args,**kwargs)
                    lock_dic[lockname] = -1
                except:
                    data = {"status":lock_dic[lockname]}
                    lock_dic[lockname] = 0
                finally:
                    return data
            else:
                return {"status":lock_dic[lockname]}
        return verify_func
    return verify

@xlock("pic")
def pic():
    return "pic"

#
# print pic()
# print lock_dic
# print pic()
import time
now = time.time()
print type(now)
# print time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(now))

with open("/tmp/.cache",'r+') as f:
    f.seek(13,0)
    print f.read()
    f.close()

