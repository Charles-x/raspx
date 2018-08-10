#!/usr/bin/env python
#coding:utf-8


from flask import Flask,make_response,jsonify,Response
from flask_restful import Resource, Api,reqparse
from flask_cors import *
from functools import wraps
from pinfo import Pifo
from xAD import xADC
# from tinydb import TinyDB, Query
from xlogging import xlog
import os
import time
import fcntl

app = Flask(__name__)
# cross origin to access
CORS(app,supports_credentials=True)
api = Api(app)

# lock dic
lock_dic = { 'T_H': 0,'pinfo': 0,'pic': 0,'soil_H': 0,'irrigate': 0}


class xLOCK:
    def __init__(self, name='/tmp/.raspx_cached/xLOCK.L'):
        self.flock = open(name, 'w')
        self.fid = self.flock.fileno()

    def lock(self):
        try:
            fcntl.lockf(self.fid, fcntl.LOCK_SH)
            return True
        except:
            return False

    def unlock(self):
        self.flock.close()

class tool_box:
    xnote = '.xnote.dat'
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time()))
    # db = TinyDB(xnote)
    logx = xlog(xnote)
    @staticmethod
    def xinit():
        tool_box.Guestlog('System runing...',None)

    @staticmethod
    def xlock(lockname):
        def verify(func):
            @wraps(func)
            def verify_func(*args, **kwargs):
                global lock_dic
                if lock_dic[lockname] == 0:
                    lock_dic[lockname] = 1
                    try:
                        data = func(*args,**kwargs)
                        lock_dic[lockname] = 0
                    except:
                        data = {"status":lock_dic[lockname]}
                        lock_dic[lockname] = -1
                    finally:
                        return data
                else:
                    return {"status":lock_dic[lockname]}
            return verify_func
        return verify

    @staticmethod
    def xresponse(data,type):
        if type =='json':
            data = jsonify({}.update(data))
        elif type == 'image':
            type = 'image/png'
        response = make_response(data)
        response.headers['Content-Type'] = type
        return response

    @staticmethod
    def Guestlog(action,gtime):
        if gtime == None:
            ctime = str(time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time())))
        else:
            ctime = gtime
        data = {'time':ctime,'action':action}

        # xl = xLOCK()
        # xl.lock()
        # tool_box.db.insert(data)
        # xl.unlock()
        tool_box.logx.write(data)



    @staticmethod
    def Guestbook(action):
        def inner(func):
            @wraps(func)
            def logx(*args, **kwargs):
                tool_box.Guestlog(action=action,gtime=None)
                # with open(tool_box.xnote, "a+") as f:
                #     ctime = str(time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time())))
                #     xn = "\t" + action + "\n"
                #     f.write(ctime + xn)
                #     f.close()
                return func(*args, **kwargs)

            return logx

        return inner




# function list

class T_H(Resource):
    @tool_box.Guestbook("看了一次温度~")
    def get(self):
        from DHT11 import T_H
        data = T_H.auto_getdata(THpin=6)
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        return response

class pinfo(Resource):
    @tool_box.Guestbook("刷新了一下树莓派的硬件状态！")
    def get(self):
        pi = Pifo()
        data = {"status":"ok",
                'data':{"model":"Raspberry Pi 3B",
                        "cpu": pi.cpu_info,
                        "disk": pi.disk_info,
                        "mem": pi.mem_info,
                        "net": pi.net_info,
                        "uptime": pi.uptime}}
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        return response

class pic(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('resolution', type=str)

    @tool_box.Guestbook("刷新了照片！")
    def get(self):
        UPLOAD_PATH = "/home/pi/Pictures"
        filename = "test.jpg"
        image_data = open(os.path.join(UPLOAD_PATH,filename), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response


    def post(self):
        import xpicture
        picpath = '/home/pi/Pictures/test.jpg'
        get_data =self.parser.parse_args()
        picpx =get_data.setdefault('resolution',"800x600")
        pica = xpicture.xpic(picpath, picpx)
        try:
            pic_data = pica.capture()
            tool_box.Guestlog("照了一张{}的植物照片~".format(picpx),None)
        except Exception as e :
            return e
        pic_upload_link = 'http://vps.sea.ink'
        data = pic_data.update({'link':pic_upload_link})
        response = make_response(jsonify(pic_data))
        response.headers['Content-Type'] = 'application/json'
        return response

class soil_H(Resource):
    @tool_box.Guestbook("看了看光线亮度，感受下土壤湿度...")
    def get(self):
        ad = xADC()
        data = ad.interpret()
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        return response

class irrigate(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('second', type=int)

    def get(self):
        data = {'status':'error'}
        get_data =self.parser.parse_args()
        tm =get_data.setdefault('second',1)
        from relay import Relay
        rp = Relay(pin=5)
        try:
            rp.connect(tm)
            tool_box.Guestlog("浇水了一次，浇了{}秒钟！！".format(tm),None)
            data.update({'status':'ok','second':tm})
        except:
            data.update({'second':tm})
        finally:
            response = make_response(jsonify(data))
            response.headers['Content-Type'] = 'application/json'
            return response

class Guest_log(Resource):
    def get(self):
        data = tool_box.logx.read()
        # data = tool_box.db.all()
        response = make_response(jsonify({'data':data}))
        response.headers['Content-Type'] = 'application/json'
        return response


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, location='json')
        self.parser.add_argument("password", type=str, location='json')
        # self.parser.add_argument('password', location=['json', 'args'],type=json,required = True,action='append')
        pass

    def get(self):
        return

    def post(self):
        # json_data = request.get_json(force=True)
        # print json_data
        get_data = self.parser.parse_args()
        print get_data
        data = {'status':None,'token':None}
        username = get_data.setdefault('username',None)
        password = get_data.setdefault('password',None)
        if username =="admin" and password =="admin":
            token = "abcd"
            data =  {'status':True,'token':token}
            response = make_response(jsonify(data))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            data = {'status':False,'token':None}
            response = make_response(jsonify(data))
            response.headers['Content-Type'] = 'application/json'
            return response



   # System init
tool_box.xinit()



# resource list
api.add_resource(T_H, '/T_H')
api.add_resource(pic,"/pic")
api.add_resource(pinfo,"/pinfo")
api.add_resource(soil_H,"/soil_H")
api.add_resource(irrigate,"/irrigate")
api.add_resource(Guest_log,"/Guest_log")
api.add_resource(Login,"/Login")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)