#!/usr/bin/env python
# coding:utf-8
from functools import wraps

# -1 = ready, 1 = using, 0 = error
lock_dic = {'T_H': -1, 'pinfo': -1, 'pic': -1, 'soil_H': -1, 'irrigate': -1}


def xlock(lockname):
    def verify(func):
        @wraps(func)
        def verify_func(*args, **kwargs):
            global lock_dic
            if lock_dic[lockname] == -1:
                lock_dic[lockname] = 1
                try:
                    data = func(*args, **kwargs)
                    lock_dic[lockname] = -1
                except:
                    data = {"status": lock_dic[lockname]}
                    lock_dic[lockname] = 0
                finally:
                    return data
            else:
                return {"status": lock_dic[lockname]}

        return verify_func

    return verify


import os
import time


def Guestbook(action):
    xnote = '.xnote.dat'
    if not os.path.isfile(xnote):
        open(xnote, 'w').close()

    def inner(func):
        @wraps(func)
        def logx(*args, **kwargs):
            with open(xnote, "a+") as f:
                ctime = str(time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(Now)))
                xn = "\t" + action + "\n"
                f.write(ctime + xn)
                f.close()
            return func(*args, **kwargs)

        return logx

    return inner


from tinydb import TinyDB

db = TinyDB('/tmp/test.db')
action = "看了一次温度~"
nowtime = time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time()))
db.insert({'time': nowtime, 'action': action})
