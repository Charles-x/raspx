#!/usr/bin/env python
#coding:utf-8


from flask import Flask,make_response,jsonify,Response
from flask_restful import Resource, Api,reqparse
from flask_cors import *
from functools import wraps
from pinfo import Pifo
from PCF8591 import xADC

import os
import time

app = Flask(__name__)
# cross origin to access
CORS(app,supports_credentials=True)
api = Api(app)

# lock dic
lock_dic = { 'T_H': 0,'pinfo': 0,'pic': 0,'soil_H': 0,'irrigate': 0}


class tool_box:

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
        if type =='application/json':
            data = jsonify({}.update(data))
        response = make_response(data)
        response.headers['Content-Type'] = type
        return response

# function list

class T_H(Resource):
    def get(self):
        from DHT11 import T_H
        data = T_H.auto_getdata(THpin=6)
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        return response

class pinfo(Resource):
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
        pica = xpicture.xpic(picpath, "800x600")
        try:
            pic_data = pica.capture()
        except Exception as e :
            return e
        pic_upload_link = 'http://vps.sea.ink'
        data = pic_data.update({'link':pic_upload_link})
        response = make_response(jsonify(pic_data))
        response.headers['Content-Type'] = 'application/json'
        return response

class soil_H(Resource):
    def get(self):
        ad = xADC()
        data = ad.auto_read()
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
            data.update({'status':'ok','second':tm})
        except:
            data.update({'second':tm})
        finally:
            response = make_response(jsonify(data))
            response.headers['Content-Type'] = 'application/json'
            return response


# resource list
api.add_resource(T_H, '/T_H')
api.add_resource(pic,"/pic")
api.add_resource(pinfo,"/pinfo")
api.add_resource(soil_H,"/soil_H")
api.add_resource(irrigate,"/irrigate")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)