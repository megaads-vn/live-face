from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import cv2

RESPONSE = {
    'status': 'successful'
}

class LiveFaceOffCamera(Resource):

    def post(self):
        cam = cv2.VideoCapture(0)
        if cam.isOpened() == True:
            file = open('camera.lock', 'w+')

        return RESPONSE
