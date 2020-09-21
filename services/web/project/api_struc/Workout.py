from flask_restful import Resource
from flask import request, jsonify
from models import Workout, Action
# We need the db object! ahhhhhhhhhh => move it to models.py?! then app needs to import it. is it still the same object if manage.py is then initializing it again when loading models.py? But probably its doing that already anyways..


class Workout(Resource):
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

    def delete(self):
        pass