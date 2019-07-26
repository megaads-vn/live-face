from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
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
