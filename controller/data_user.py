from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()

RESPONSE = {
    'status': 'successful',
}
class DataUser(Resource):
    def get(self):
        RESPONSE['items'] = [{'id': 1, "name": "Tung"},
                            {'id': 2, "name": "Tien Anh"},
                            {'id': 3, "name": "Diem"}]
        return RESPONSE
