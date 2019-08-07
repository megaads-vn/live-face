from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from controller.live_face_data_set import LiveFaceDataSet
from controller.live_face_training import LiveFaceTraining
from controller.live_face_recognition import LiveFaceRecognition
from controller.live_face_off_camera import LiveFaceOffCamera
from controller.data_user import DataUser

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

api.add_resource(LiveFaceDataSet, '/live-face-data-set')
api.add_resource(LiveFaceTraining, '/live-face-training')
api.add_resource(LiveFaceRecognition, '/live-face-recognition')
api.add_resource(LiveFaceOffCamera, '/live-face-off-camera')
api.add_resource(DataUser, '/data-users')

if __name__ == '__main__':
    #app.run(ssl_context='adhoc')
    app.run(debug=True)
