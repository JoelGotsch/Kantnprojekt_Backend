from flask_restful import Resource
from flask import request, jsonify
from .models import db, Exercise, Workout
import random
import string

class Test(Resource):
    def get(self):
        return({"message": "success1"}, 201)
        # try:
        #     wos = Workout.query.filter_by(user_id=1).all()#
        #     result={str(wo.id): wo.serialize() for wo in wos}
        #     print(request.headers.get("start_date"))
        #     print(request.headers.get("end_date"))
        #     print(request.headers.get("username"))
        #     return(jsonify(result))
        # except Exception as e:
        #     print("Error accessing the database")
        #     print(e)
        #     return(jsonify({"message": str(e)}), 201)

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