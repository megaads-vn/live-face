from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import cv2
import os
import numpy as np
from PIL import Image
import sys
import requests
import configparser

RESPONSE = {
    'status': 'successful'
}
config = configparser.ConfigParser()
config.read('./cfgs.ini')
urlResource = config['DEFAULT']['urlResource']

class LiveFaceRecognition(Resource):

    def buildDataFace(self):
        r = requests.get(urlResource)
        output = r.json()
        retVal = {};
        if output['status'] == 'successful':
            for item in output['items']:
                retVal[item['id']] = item['name']

        return retVal

    def delete(self):
        cam = cv2.VideoCapture(0)
        if cam.isOpened() == True:
            file = open('camera.lock', 'w+')


    def post(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('././trainer/trainer.yml')
        cascadePath = "././cascades/haarcascade_frontalface_default.xml";
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX
        users = self.buildDataFace()
        id = 0;
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 1280) # set video widht
        cam.set(4, 720) # set video height
        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                if (confidence < 100):
                    name = users[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    name = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

            cv2.imshow('camera',img)
            cv2.waitKey(10)
            if os.path.exists('camera.lock'):
                os.remove('camera.lock');
                break

        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

        return RESPONSE
