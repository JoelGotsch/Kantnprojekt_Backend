from flask_restful import Resource
from flask import request, jsonify
from .models import User, Exercise, db
import datetime
import dateutil.parser
from ..misc import funcs as funcs
# We need the db object! ahhhhhhhhhh => move it to models.py?! then app needs to import it. is it still the same object if manage.py is then initializing it again when loading models.py? But probably its doing that already anyways..


class API_Exercise(Resource):
    def get(self):
        try:
            user_id = request.headers.get("user_id")
            user = User.query.filter(User.user_id==user_id).first()
            exercises = []
            if user.token != request.headers.get("token"):
                return {"message": "Token is invalid!"}, 400
            try:
                exercise_id = request.args.get("exercise_id")
                if len()>0:
                    exercises = [Exercise.query.get(exercise_id)]
            number = int(request.args.get("number"))
            
            if len(exercises)==0:
                if number == 0:
                    exercises = Exercise.query.filter_by(user_id = user_id).all()
                else:
                    exercises = Exercise.query.filter_by(user_id = user_id).limit(number).all()
                # wos2 = Workout.query.filter_by(last_edit >= start_date, last_edit <= end_date, user_id = user_id).all()

            result = {ex.id: ex.serialize() for ex in exercises}
            return(jsonify(result))

        except Exception as e:
            return jsonify({"message":  str(e)}, 400)

    def post(self):
        # has to have
        response = {}
        try:
            token = request.headers.get("token")
            user_id = request.headers.get("user_id")
            # firebase_id_token=request.args.get("firebase_id_token")
            # verify the id token with firebase admin package! only then return api key.
            auth_ok = bool(User.query.filter_by(
                id=user_id, token=token).count())
        except Exception as e:
            return jsonify({"message":  str(e)}, 400)

        if not auth_ok:
            return(({"status": "failure", "message": "Authentication didn't work"}), 400)

        user = User.query.filter_by(id=user_id).first()

        data = request.get_json(force=True)  # should be a dict
        print("incoming exercise data: "+str(data))
        try:
            for ex_id in data:
                # check if ex_id is already created, so we only need to update it:
                ex = Exercise.query.filter_by(id=ex_id, user_id=user_id).first()
                json_ex = data[ex_id]
                if len(ex) > 0: # updating existing exercise
                    ex.note = json_ex["note"]
                    ex.not_deleted = json_ex["not_deleted"]
                    response[json_ex["local_id"]] = ex.id
                    db.session.commit() 
                else: # creating a new exercise
                    ex = Exercise(user_id=user_id,
                                date=dateutil.parser.parse(json_ex["date"]),
                                title=json_ex["title"],
                                note=json_ex["note"],
                                last_edit=dateutil.parser.parse(
                                    json_ex["last_edit"]),
                                not_deleted=dateutil.parser.parse(
                                    json_ex["not_deleted"]),
                                unit=json_ex["unit"],
                                points=json_ex["points"],
                                max_points_day=json_ex["max_points_day"],
                                weekly_allowance=json_ex["weekly_allowance"],
                                )
                    
                    db.session.add(ex)
                    db.session.commit()
                    response[json_ex["local_id"]] = ex.id
            return({"status": 'success', 'data': response}, 201)
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self): # done via "not_deleted" = False 
        pass
