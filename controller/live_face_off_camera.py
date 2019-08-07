from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask import Response
import os

RESPONSE = {
    'status': 'successful'
}

class LiveFaceOffCamera(Resource):

    def post(self):
        if os.path.exists('camera.lock'):
            os.remove('camera.lock')

        file = open('camera.lock', 'w+')

        return RESPONSE

    def options(self):
        resp = Response("")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = '*'

        return resp
