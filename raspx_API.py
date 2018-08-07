#!/usr/bin/env python
#coding:utf-8


from flask import Flask,make_response,jsonify,Response
from flask_restful import Resource, Api
from flask_cors import *
from pinfo import Pifo

import os
import time

app = Flask(__name__)
CORS(app,supports_credentials=True)
api = Api(app)

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
        data = {"cpu": pi.cpu_info,
                "disk": pi.disk_info,
                "mem": pi.mem_info,
                "net": pi.net_info,
                "uptime": pi.uptime}
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
        import camera
        return

class soil_H(Resource):
    def get(self):
        return "building..."



api.add_resource(T_H, '/T_H')
api.add_resource(pic,"/pic")
api.add_resource(pinfo,"/pinfo")
api.add_resource(soil_H,"/soil_H")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)