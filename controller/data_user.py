from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()

RESPONSE = {
    'status': 'successful',
}
class DataUser(Resource):
    def get(self):
        RESPONSE['items'] = [{'id': 1, "name": "Ha"},
                            {'id': 2, "name": "Tung"},
                            {'id': 3, "name": "Phu"},
                            {'id': 4, "name": "Tuan"},
                            {'id': 5, "name": "Bach"},
                            {'id': 6, "name": "Quan"},
                            {'id': 7, "name": "Lap"},
                            {'id': 8, "name": "Diem"},
                            {'id': 9, "name": "Zippy"},
                            {'id': 10, "name": "Tuyen"},
                            {'id': 11, "name": "Tien Anh"}
                            ]
        return RESPONSE
