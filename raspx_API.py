#!/usr/bin/env python
#coding:utf-8


from flask import Flask,make_response,jsonify,Response
from flask_restful import Resource, Api
from picamera import PiCamera

import os
import time

app = Flask(__name__)
api = Api(app)
api = Api(app)

class T_H(Resource):
    def get(self):
        import T_H
        T = T_H.T_H(THpin=6)
        data = T.auto_getdata()
        return jsonify(data)

class picture(Resource):
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


api.add_resource(T_H, '/T_H')
api.add_resource(picture,"/pic")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)