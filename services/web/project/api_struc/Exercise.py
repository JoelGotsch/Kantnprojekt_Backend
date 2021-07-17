from flask_restful import Resource
from flask import request, jsonify
from .models import User, Exercise, UserExercise, ChallengeExercise, db
import datetime
import dateutil.parser
from ..misc import funcs as funcs
import logging
# We need the db object! ahhhhhhhhhh => move it to models.py?! then app needs to import it. is it still the same object if manage.py is then initializing it again when loading models.py? But probably its doing that already anyways..

class API_Exercise(Resource):
    def get(self):
        logging.info("Get Exercise: Start")
        common_exercises_dict = {}
        user_exercises_dict = {}
        challenge_exercises_dict = {}
        try:
            token = request.headers.get("token")
            user = User.query.filter(User.token == token).first()
            logging.info(f"Get Exercise: request from {user.user_name=} {user.id=}")
            logging.debug(f"Get Exercise: {request=}")
            if user is None:
                logging.exception("Get Exercise: Token is invalid!")
                return {"status": "failure","message": "Token is invalid!"}, 400
            try:
                latest_edit_date = dateutil.parser.parse(
                    request.values.get("latest_edit_date"))
            except:
                latest_edit_date = datetime.datetime.min
            try:
                 # is used when one wants to check for missing exercises before latest_edit_date as much fewer data needs to be transferred:
                latest_edit_date_only = request.values.get("latest_edit_date_only") == "true"
            except:
                latest_edit_date_only = False
            try:
                exercise_ids = request.values.get("exercise_ids").split(",")
            except:
                exercise_ids = []
            try:
                user_exercise_ids = request.values.get("user_exercise_ids").split(",")
            except:
                user_exercise_ids = []
            logging.debug(
                f"Get Exercise: {user.user_name=}, {latest_edit_date=}, {exercise_ids=}, {user_exercise_ids=}, {latest_edit_date_only=}")
            admin_user = User.query.filter_by(user_name="kantnprojekt").first()
            if (len(exercise_ids) == 0):
                ex_list = [Exercise.query.get(ex.exercise_id) for ex in admin_user.exercises if ex.latest_edit >= latest_edit_date]
            else:
                ex_list = [Exercise.query.get(ex_id) for ex_id in exercise_ids] 

            if (len(user_exercise_ids) == 0):
                us_ex_list = [ex for ex in user.exercises if ex.latest_edit >= latest_edit_date]
            else:
                us_ex_list = [ex for ex in user.exercises if ex.id in user_exercise_ids] 

            if latest_edit_date_only:
                common_exercises_dict = {ex.id: ex.latest_edit.isoformat() for ex in ex_list if ex is not None}
                user_exercises_dict = {ex.id: ex.latest_edit.isoformat() for ex in us_ex_list if ex is not None}
                for userchallenge in user.challenges:
                    challenge_exercises = userchallenge.challenge.exercises
                    challenge_exercises_dict[userchallenge.challenge.id] = {ex.id: ex.latest_edit.isoformat() for ex in challenge_exercises if ex.latest_edit >= latest_edit_date}
            else: 
                common_exercises_dict = {ex.id: ex.serialize() for ex in ex_list if ex is not None}
                user_exercises_dict = {ex.id: ex.serialize() for ex in us_ex_list if ex is not None}
                for userchallenge in user.challenges:
                    challenge_exercises = userchallenge.challenge.exercises
                    challenge_exercises_dict[userchallenge.challenge.id] = {ex.id: ex.serialize() for ex in challenge_exercises if ex.latest_edit >= latest_edit_date}
            response = {"common_exercises": common_exercises_dict,
                      "user_exercises": user_exercises_dict,
                      "challenge_exercises": challenge_exercises_dict}
            logging.debug(f"Get Exercise: {response=}")
            return({"status": "success", "data":  response}, 201)

        except Exception as e:
            logging.exception(f"Get Exercise: {e=}")
            return ({"status": "failure", "message":  str(e)}, 400)

    def post(self):
        # should be a dict like common_exercises_dict. Automatically creates then the common_exercise and the user_exercise.
        # returns a dict with sub-dicts common_exercises and user_exercises where instead of the exercise data the id is sent (is used to update local id)
        response = {"user_exercises": {}, "common_exercises": {}}
        try:
            token = request.headers.get("token")
            user = User.query.filter_by(token=token).first()
            if user is None:
                logging.exception("Post Exercise: Authentication didn't work")
                return(({"status": "failure", "message": "Authentication didn't work"}), 400)
        except Exception as e:
            logging.exception(f"Post Exercise: {e=}")
            return ({"status": "failure", "message":  str(e)}, 400)

        data = request.get_json(force=True)  
        logging.debug(f"Post Exercise: {data=}")
        try:
            for us_ex_id in data:
                json_ex = data[us_ex_id]
                ex_id = json_ex.get("exercise_id")
                # check if ex_id is already created, so we only need to update it:
                note = json_ex.get("note")
                points = json_ex.get("points")
                max_points_day = json_ex.get("max_points_day")
                max_points_week = json_ex.get("max_points_week")
                daily_allowance = json_ex.get("daily_allowance")
                weekly_allowance = json_ex.get("weekly_allowance")
                private = json_ex.get("private", False)
                latest_edit = dateutil.parser.parse(json_ex.get("latest_edit"))
                local_id = json_ex.get("local_id")
                title = json_ex.get("title")
                description = json_ex.get("description")
                unit = json_ex.get("unit")
                checkbox = json_ex.get("checkbox", False)
                checkbox_reset = json_ex.get("checkbox_reset", 2)
                logging.debug(
                    f"Post Exercise: {note=}, {points=}, {max_points_day=}, {max_points_week=}, {daily_allowance=}, {weekly_allowance=}, {private=}, {latest_edit=}, {local_id=}, {title=}, {description=}, {unit=}, {checkbox=}, {checkbox_reset=}")
                us_ex = UserExercise.query.get(us_ex_id)
                if us_ex is not None:  # updating existing user exercise
                    # if the user created the exercise, he can update some more infos like the notes
                    logging.debug("Post Exercise: Updating User-Exercise")
                    us_ex.note = note
                    us_ex.points = points
                    us_ex.max_points_day = max_points_day
                    us_ex.max_points_week = max_points_week
                    us_ex.daily_allowance = daily_allowance
                    us_ex.weekly_allowance = weekly_allowance
                    us_ex.private = private
                    us_ex.latest_edit = latest_edit
                    response["user_exercises"][local_id] = us_ex.id
                    db.session.commit()
                else:  # creating a new user exercise (and Exercise if it is linked to a non-existent one)
                    logging.debug("Post Exercise: Creating new exercise and User Exercises")
                    ex = Exercise.query.filter_by(title = title).first()
                    if ex is not None:
                        logging.warning(f"Post Exercise: Exercise with that {title=} already exists. Choose a different title.")
                        response["common_exercises"][local_id] = ex.id
                        response["user_exercises"][local_id] = {"status": "failure", "message": "Exercise with that title already exists. Choose a different title."}
                        continue
                    # completely new exercise
                    ex = Exercise(
                        title=title,
                        note=note,
                        description=description,
                        user_id=user.id,
                        unit=unit,
                        points=points,
                        max_points_day=max_points_day,
                        max_points_week=max_points_week,
                        daily_allowance=daily_allowance,
                        weekly_allowance=weekly_allowance,
                        checkbox=checkbox,
                        checkbox_reset=checkbox_reset,
                        latest_edit=latest_edit,
                    )
                    db.session.add(ex)
                    db.session.commit()
                    # creating user exercise for every user:
                    for other_user in User.query.all():
                        us_ex = UserExercise(
                            note=note,
                            exercise_id = ex.id,
                            user_id=other_user.id,
                            user=other_user,
                            points=points,
                            max_points_day=max_points_day,
                            max_points_week=max_points_week,
                            daily_allowance=daily_allowance,
                            weekly_allowance=weekly_allowance,
                            latest_edit=latest_edit,
                            private=private,
                        )
                        db.session.add(us_ex)
                        db.session.commit()
                    response["common_exercises"][local_id] = ex.id
                    response["user_exercises"][local_id] = us_ex.id
            logging.debug(f"Post Exercise: {response=}")
            return({"status": 'success', 'data': response}, 201)
        except Exception as e:
            logging.exception(f"Post Exercise: Could not read json or header. {e=}")
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self):  # done via "not_deleted" = False
        pass
