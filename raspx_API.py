#!/usr/bin/env python
#coding:utf-8


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class T_H(Resource):
    def get(self):
        import T_H

        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)