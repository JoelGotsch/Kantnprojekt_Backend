from flask_restful import Resource
from flask import request
from models import db
import random
import string

class Test(Resource):
    def get(self):
        return { "status" : "success"}, 200

    def post(self):
        result={"test": "test23"}
        try:
            header = request.headers["Authorization"]
            json_data = request.get_json(force=True)
            result = json_data
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)
        return({ "status": 'success', 'data': result }, 201)