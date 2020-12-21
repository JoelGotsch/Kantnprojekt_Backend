

# get details of challenge
# create new challenge
# token needed
# user join challenge
# token needed

from flask_restful import Resource
from flask import request
from .models import ChallengeExercise, Exercise, UserChallenge, Workout, User, Action, Challenge, db
import datetime
import dateutil.parser
from ..misc import funcs as funcs


class API_Challenges(Resource):
    # get list of challenges
    #  no token needed
    def get(self):
        try:
            detail_level = request.values.get("detail_level", "headers") # could be "headers", "info" or "details"
            if detail_level == "headers":
                challenges_dict = {ch.id: ch.headers() for ch in Challenge.query.filter(
                    Challenge.end_date >= datetime.datetime.now()).all()}
            elif detail_level == "info":
                challenges_dict = {ch.id: ch.serialize() for ch in Challenge.query.filter(
                    Challenge.end_date >= datetime.datetime.now()).all()}
            elif detail_level == "details":
                challenges_dict = {ch.id: ch.details() for ch in Challenge.query.filter(
                    Challenge.end_date >= datetime.datetime.now()).all()}
            else:
                raise("Getting challenges-info: detail level unknown: "+ detail_level)
            return({"status": "success", "data": challenges_dict}, 201)
        except Exception as e:
            return ({"status": "failure", "message":  str(e)}, 400)

class API_ChallengeAccept(Resource):
    # user subscribes to challenge
    def get(self):
        try:
            token = request.headers.get("token")
            # firebase_id_token=request.values.get("firebase_id_token")
            # verify the id token with firebase admin package! only then return api key.
            user = User.query.filter_by(token=token).first()
            if user is None:
                return(({"status": "failure", "message": "Authentication didn't work"}), 400)
            challenge_id = request.values.get("challenge_id", "")
            start_date = dateutil.parser.parse(request.values.get("start_date", datetime.datetime.now().isoformat()))
            if challenge_id is None or start_date is None:
                raise("Challenge id or start date for accepting the challenge was not provided.")
            ch= Challenge.query.get(challenge_id)
            if ch is None:
                raise("Couldn't find challenge id "+ str(challenge_id))
            user_ch = UserChallenge(
                    user_id=user.id, challenge_id=ch.id, user_start_challenge=start_date)
            # user_ch.challenge.append(ch)
            ch.users.append(user_ch)
            db.session.add(user_ch)
            db.session.commit()
            return({"status": "success", "data": user_ch.serialize()}, 201)
        except Exception as e:
            return ({"status": "failure", "message":  str(e)}, 400)

class API_Challenge(Resource):
    def get(self):
        try:
            challenge_id = request.values.get("challenge_id")
            if challenge_id is None or challenge_id == "":
                raise("No challenge id provided")
            challenge = Challenge.query.get(challenge_id)
            return({"status": "success", "data": challenge.details()}, 201)

        except Exception as e:
            return ({"status": "failure", "message":  str(e)}, 400)

    def post(self):
        # has to have unique name, start_date, end_date, description, exercises, eval_period
        # returns challenge_id, challenge_exercise ids

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
        print("incoming challenge creation data: "+str(data))
        try:
            json_ch = data
            new_ch_id = funcs.rand_string(30)
            start_date = dateutil.parser.parse(json_ch["start_date"])
            end_date = dateutil.parser.parse(json_ch["end_date"])
            name = json_ch["name"]
            description = json_ch["description"]
            min_points = json_ch["min_points"]
            eval_period = json_ch["eval_period"] # could be "day", "week", "month", "year"
            ch = Challenge(id=new_ch_id,
                            name=name,
                            description=description,
                            start_date=start_date,
                            end_date=end_date,
                            min_points=min_points,
                            eval_period=eval_period,
                            )
            response["challenge_id"] = new_ch_id
            db.session.add(ch)
            db.session.commit()
            # TODO: go through list of users of provided json
            user_ch = UserChallenge(
                user_id=user.id, challenge_id=new_ch_id, user_start_challenge=start_date)
            ch.users.append(user_ch)
            db.session.add(user_ch)
            db.session.commit()
            # add exercises
            json_exercises = json_ch["exercises"]
            response["exercises"] = {}
            for ch_ex_key in json_exercises:
                json_ex = json_exercises[ch_ex_key]
                ch_ex_id = funcs.rand_string(30)
                exercise_id = json_ex["exercise_id"]
                ex = Exercise.query.get(exercise_id)
                if ex is None:
                    raise("Couldn't find exercise with id "+exercise_id)
                note = json_ex["note"]
                points = json_ex["points"]
                max_points_day = json_ex["max_points_day"]
                max_points_week = json_ex["max_points_week"]
                daily_allowance = json_ex["daily_allowance"]
                weekly_allowance = json_ex["weekly_allowance"]
                ch_ex = ChallengeExercise(
                    id=ch_ex_id,
                    exercise_id=exercise_id,
                    challenge_id=ch.id,
                    points=points,
                    max_points_day=max_points_day,
                    max_points_week=max_points_week,
                    daily_allowance=daily_allowance,
                    weekly_allowance=weekly_allowance,
                    note=note,
                    latest_edit=datetime.datetime.now(),
                )
                ch.exercises.append(ch_ex)
                db.session.add(ch_ex)
                db.session.commit()
                response["exercises"][exercise_id] = ch_ex_id
            return({"status": 'success', 'data': response}, 201)
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self):  # done via "not_deleted" = False
        pass
