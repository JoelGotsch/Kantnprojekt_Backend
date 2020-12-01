from typing import NoReturn
from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy.sql.elements import Null
from .models import Exercise, Workout, User, Action, db
import datetime
import dateutil.parser
from ..misc import funcs as funcs
# We need the db object! ahhhhhhhhhh => move it to models.py?! then app needs to import it. is it still the same object if manage.py is then initializing it again when loading models.py? But probably its doing that already anyways..


class API_Workout(Resource):
    def get(self):
        try:
            token = request.headers.get("token")
            user = User.query.filter(User.token == token).first()
            wos = []
            if user is None:
                return {"message": "Token is invalid!"}, 400
            try:
                workout_id = request.values.get("workout_id")
                if workout_id is not None and len(workout_id) > 0:
                    wos = [Workout.query.get(workout_id)]
            except:
                wos = []
            try:
                latest_edit_date = dateutil.parser.parse(
                    request.values.get("latest_edit_date"))
            except:
                latest_edit_date = datetime.datetime.min
            try:
                start_date = dateutil.parser.parse(
                    request.values.get("start_date"))
            except:
                start_date = datetime.datetime.min
            try:
                end_date = dateutil.parser.parse(
                    request.values.get("end_date"))
            except:
                end_date = datetime.datetime.now()
            try:
                number = int(request.values.get("number"))
            except:
                number = 0
            try:
                latest_edit_date_only = bool(
                    request.values.get("latest_edit_date_only"))
            except:
                latest_edit_date_only = False
            if len(wos) == 0:
                if number == 0:
                    wos = Workout.query.filter(
                        Workout.date >= start_date,  Workout.date <= end_date, Workout.user_id == user.id, Workout.latest_edit >= latest_edit_date).all()
                else:
                    wos = Workout.query.filter(Workout.date >= start_date, Workout.date <= end_date,
                                               Workout.user_id == user.id, Workout.latest_edit >= latest_edit_date).limit(number).all()
                    # wos = Workout.query.filter(
                    #     Workout.date >= start_date and Workout.date <= end_date and Workout.user_id==user.id).limit(number).all()
                    # wos = Workout.query.filter_by(
                    #     date >= start_date, date <= end_date, user_id=user.id).limit(number).all()
                # wos2 = Workout.query.filter_by(latest_edit >= start_date, latest_edit <= end_date, user_id = user_id).all()
            if latest_edit_date_only:
                result = {wo.id: wo.latest_edit.isoformat() for wo in wos}
            else:
                result = {wo.id: wo.serialize() for wo in wos}
            return(result)

        except Exception as e:
            return ({"message":  str(e)}, 400)

    def post(self):
        # has to have
        response = {}
        try:
            token = request.headers.get("token")
            # firebase_id_token=request.values.get("firebase_id_token")
            # verify the id token with firebase admin package! only then return api key.
            user = User.query.filter_by(token=token).first()
            if user is None:
                return(({"status": "failure", "message": "Authentication didn't work"}), 400)
        except Exception as e:
            return ({"message":  str(e)}, 400)

        data = request.get_json(force=True)  # should be a dict
        print("incoming workout data: "+str(data))
        try:
            for wo_id in data:
                # check if wo_id is already created, so we only need to update it:
                wo = Workout.query.filter_by(id=wo_id, user_id=user.id).first()
                json_wo = data[wo_id]
                if wo is not None:  # updating existing workout
                    if not json_wo["not_deleted"]:
                        db.session.delete(wo)
                        db.session.commit()
                        response[json_wo["local_id"]] = ""
                        continue
                    wo.date = dateutil.parser.parse(json_wo["date"])
                    wo.note = json_wo["note"]
                    wo.latest_edit = dateutil.parser.parse(
                        json_wo.get("latest_edit"))
                    # removing and adding each of the actions!
                    # for ac in wo.actions:
                    #     db.session.delete(ac)
                    #     db.session.commit()
                    for ac in wo.actions:
                        db.session.delete(ac)
                    db.session.commit()
                    # wo.actions.delete() # TODO: only delete actions which are not resent and don't re-create them below.
                    for ac_key in json_wo["actions"]:
                        # check if action is already in database:
                        if Action.query.get(ac_key) is not None:
                            continue
                        json_ac = json_wo["actions"][ac_key]
                        # TODO: This block is not necessary if the database is permanent and new exercises are uploaded directly. Should instead throw an error that the exercise is not known?
                        # check if exercise exists already:

                        if Exercise.query.get(json_ac["exercise_id"]) is None:
                            return(({"status": "failure", "message": "Exercise " + json_ac["exercise_id"] + " from workout "+json_wo['local_id']+" is not stored on the server."}), 400)

                        ac = Action(id=ac_key, exercise_id=json_ac["exercise_id"], workout_id=wo.id,
                                    number=json_ac["number"], note=json_ac["note"])
                        wo.actions.append(ac)
                        db.session.add(ac)
                        db.session.commit()

                    response[json_wo["local_id"]] = wo.id
                    db.session.commit()
                else:  # creating a new workout
                    new_wo_id = funcs.rand_string(30)
                    wo = Workout(id=new_wo_id,
                                 user_id=user.id,
                                 date=dateutil.parser.parse(json_wo["date"]),
                                 note=json_wo["note"],
                                 latest_edit=dateutil.parser.parse(
                                     json_wo["latest_edit"]),
                                 )
                    response[json_wo["local_id"]] = new_wo_id
                    db.session.add(wo)
                    db.session.commit()
                    for ac_key in json_wo["actions"]:
                        json_ac = json_wo["actions"][ac_key]
                        if Exercise.query.get(json_ac["exercise_id"]) is None:
                            return(({"status": "failure", "message": "Exercise {exercise_id} from workout "+json_wo['local_id']+" is not stored on the server."}), 400)

                        ac = Action(id=funcs.rand_string(30), exercise_id=json_ac["exercise_id"], workout_id=wo.id,
                                    number=json_ac["number"], note=json_ac["note"])
                        wo.actions.append(ac)
                        db.session.add(ac)
                        db.session.commit()
            return({"status": 'success', 'data': response}, 201)
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self):  # done via "not_deleted" = False
        pass
