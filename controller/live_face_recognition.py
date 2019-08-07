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

RESPONSE = {
    'status': 'successful'
}
config = configparser.ConfigParser()
config.read('./cfgs.ini')
urlResource = config['DEFAULT']['urlHrm'] + '/service/staff/data-staff?token=' + config['DEFAULT']['token']
#urlResource = 'http://127.0.0.1:5000/data-users'
apiTimeKeeping = config['DEFAULT']['urlHrmApi'] + '/api/staff/send-finger-print'

class LiveFaceRecognition(Resource):

    def buildDataFace(self):
        r = requests.get(urlResource, verify=False)
        output = r.json()
        print("\n Output=" + output)
        retVal = {};
        if output['status'] == 'successful':
            for item in output['items']:
                retVal[item['id']] = item['name']

        return retVal

    def post(self):
        #recognizer = cv2.face.LBPHFaceRecognizer_create() #working on Mac or Pc
        recognizer = cv2.face.createLBPHFaceRecognizer() #working on Pi
        recognizer.load('././trainer/trainer.yml') # recognizer.read() working on Mac or Pc, .load() worked on Pi
        cascadePath = "././cascades/haarcascade_frontalface_default.xml";
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX
        users = self.buildDataFace()
        id = 0;
        if os.path.exists('camera.lock'):
            os.remove('camera.lock')
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height
        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        timeKeeping = {}
        for user in users:
            timeKeeping[user] = []

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)))
            target = 0
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                if (confidence < 100):
                    name = ''
                    if id in users:
                        name = users[id]
                        target = round(100 - confidence)
                        # if target >= 50:
                        #     timeKeeping[id].append(target)
                        #
                        # if len(timeKeeping[id]) >= 50:
                        #     # post a timeKeeping
                        #     try:
                        #         r = requests.post(apiTimeKeeping, data={"staff_id": id})
                        #         if r.status_code == 200:
                        #             timeKeeping[id] = []
                        #     except:
                        #         print("An exception occurred")

                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    name = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                if target >= 50:
                    cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                    cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

            cv2.imshow('camera',img)
            cv2.waitKey(10)
            if os.path.exists('camera.lock'):
                os.remove('camera.lock')
                break

        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

        return RESPONSE

    def options(self):
        resp = Response("")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = '*'

        return resp
