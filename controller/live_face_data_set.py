from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import cv2
import os

parser = reqparse.RequestParser()
dir = '././dataset/'
if os.path.isdir(dir) == False:
    os.mkdir(dir)

RESPONSE = {
    'status': 'successful'
}

class LiveFaceDataSet(Resource):
    def get(self):
        return RESPONSE

    def post(self):
        parser.add_argument('id')
        args = parser.parse_args()
        face_id = args['id']
        path =  dir + face_id
        if os.path.isdir(path):
            list_images = os.listdir(path)
            for image in list_images:
                os.remove(path + '/' + image);
        else:
            os.mkdir(path)

        if os.path.exists('camera.lock'):
            os.remove('camera.lock')

        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        face_detector = cv2.CascadeClassifier('././cascades/haarcascade_frontalface_default.xml')
        # For each person, enter one numeric face id
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        count = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5, 20)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite(path + "/user." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)
            cv2.waitKey(50)
            if count >= 30: # Take 30 face sample and stop video
                break
            elif os.path.exists('camera.lock'):
                os.remove('camera.lock')
                break

        cam.release()
        cv2.destroyAllWindows()

        return RESPONSE
