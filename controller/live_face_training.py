from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask import Response
import cv2
import os
import numpy as np
from PIL import Image
import sys
import requests
import configparser

config = configparser.ConfigParser()
config.read('./cfgs.ini')
urlResource = config['DEFAULT']['urlHrm'] + '/service/staff/data-staff?token=' + config['DEFAULT']['token']
# urlResource = 'http://127.0.0.1:5000/data-users'
parser = reqparse.RequestParser()

#recognizer = cv2.face.LBPHFaceRecognizer_create() #working on Pc or Mac
recognizer = cv2.face.createLBPHFaceRecognizer() #working on pi
detector = cv2.CascadeClassifier("././cascades/haarcascade_frontalface_default.xml");
dir = '././trainer'
if os.path.isdir(dir) == False:
    os.mkdir(dir)

RESPONSE = {
    'status': 'successful'
}

class LiveFaceTraining(Resource):

    def getFaceIds(self):
        r = requests.get(urlResource, verify=False)
        output = r.json()
        retVal = [];
        if output['status'] == 'successful':
            for item in output['items']:
                retVal.append(item['id'])
        return retVal

    def post(self):
        return RESPONSE

    def get(self):
        arrIds = self.getFaceIds()
        faces,ids = self.getImagesAndLabels(arrIds)
        recognizer.train(faces, np.array(ids))
        # Save the model into trainer/trainer.yml
        recognizer.save('././trainer/trainer.yml') # recognizer.write() worked on Mac or PC, .save() worked on Pi
        RESPONSE['message'] = 'Live faces trained'
        return RESPONSE

    def getImagesAndLabels(self, arrIds):
        faceSamples=[]
        ids = []
        for id in arrIds:
            pathUser = '././dataset' + '/' + str(id)
            if os.path.isdir(pathUser):
                imagePaths = [os.path.join(pathUser,f) for f in os.listdir(pathUser)]
                for imagePath in imagePaths:
                    PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                    img_numpy = np.array(PIL_img,'uint8')
                    id = int(os.path.split(imagePath)[-1].split(".")[1])
                    faces = detector.detectMultiScale(img_numpy)
                    for (x,y,w,h) in faces:
                        faceSamples.append(img_numpy[y:y+h,x:x+w])
                        ids.append(id)

        return faceSamples,ids

    def options(self):
        resp = Response("")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = '*'

        return resp
