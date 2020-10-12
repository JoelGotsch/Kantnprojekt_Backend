from flask_restful import Resource
from flask import request, jsonify
from .models import Workout, User, Action, db
import datetime
import dateutil.parser
from ..misc import funcs as funcs
# We need the db object! ahhhhhhhhhh => move it to models.py?! then app needs to import it. is it still the same object if manage.py is then initializing it again when loading models.py? But probably its doing that already anyways..


class API_Workout(Resource):
    def get(self):
        try:
            user_id = request.headers.get("user_id")
            user = User.query.filter(User.user_id==user_id).first()
            wos = []
            if user.token != request.headers.get("token"):
                return {"message": "Token is invalid!"}, 400
            try:
                workout_id = request.args.get("workout_id")
                if len()>0:
                    wos = [Workout.query.get(workout_id)]
            try:
                start_date = dateutil.parser.parse(request.args.get("start_date"))
            except:
                start_date = datetime.datetime.min
            try:
                end_date = dateutil.parser.parse(request.args.get("end_date"))
            except:
                end_date = datetime.datetime.now()
            number = int(request.args.get("number"))
            if len(wos)==0:
                if number == 0:
                    wos = Workout.query.filter_by(date >= start_date, date <= end_date, user_id = user_id).all()
                else:
                    wos = Workout.query.filter_by(date >= start_date, date <= end_date, user_id = user_id).limit(number).all()
                # wos2 = Workout.query.filter_by(last_edit >= start_date, last_edit <= end_date, user_id = user_id).all()

            result = {wo.id: wo.serialize() for wo in wos}
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
        print("incoming workout data: "+str(data))
        try:
            for wo_id in data:
                # check if wo_id is already created, so we only need to update it:
                wo = Workout.query.filter_by(id=wo_id, user_id=user_id).first()
                json_wo = data[wo_id]
                if len(wo) > 0: # updating existing workout
                    wo.date = dateutil.parser.parse(json_wo["date"])
                    wo.note = json_wo["note"]
                    wo.last_edit = dateutil.parser.parse(
                        json_wo["last_edit"])
                    wo.not_deleted = dateutil.parser.parse(
                        json_wo["not_deleted"])
                    #removing and adding each of the actions!
                    for ac in wo.actions:
                        db.session.delete(ac)
                        db.session.commit()
                    for ac_key in json_wo:
                        json_ac = json_wo[ac_key]
                        ac = Action(id = funcs.rand_string(30), exercise_id=json_ac["exercise_id"], workout_id=wo.id,
                                    number=json_ac["number"], note=json_ac["note"])
                        wo.actions.append(ac)
                        db.session.add(ac)
                        db.session.commit() 
                    response[json_wo["local_id"]] = wo.id
                    db.session.commit() 
                else: # creating a new workout
                    new_wo_id = funcs.rand_string(30)
                    wo = Workout(id=new_wo_id,
                                user_id=user_id,
                                date=dateutil.parser.parse(json_wo["date"]),
                                note=json_wo["note"],
                                last_edit=dateutil.parser.parse(
                                    json_wo["last_edit"]),
                                not_deleted=dateutil.parser.parse(
                                    json_wo["not_deleted"]),
                                )
                    response[json_wo["local_id"]] = new_wo_id
                    db.session.add(wo)
                    db.session.commit() 
                    for ac_key in json_wo:
                        json_ac = json_wo[ac_key]
                        ac = Action(id = funcs.rand_string(30), exercise_id=json_ac["exercise_id"], workout_id=wo.id,
                                    number=json_ac["number"], note=json_ac["note"])
                        wo.actions.append(ac)
                        db.session.add(ac)
                        db.session.commit() 
            return({"status": 'success', 'data': response}, 201)
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self): # done via "not_deleted" = False 
        pass
