from flask_restful import Resource
from flask import request, jsonify
from .models import User, Exercise, UserExercise, db
import datetime
import random
from ..misc import funcs as funcs
import time
import logging


class API_User(Resource):
    def get(self):  # To get usernames of other users
        # header = request.headers["Authorization"]
        logging.info("Get User: Start")
        try:
            # email = data.get("email")
            token = request.headers.get("token")
            # firebase_id_token=data.get("firebase_id_token")
            # verify the id token with firebase admin package! only then return api key.
            user_id = request.values.get("user_id")
            auth_ok = bool(User.query.filter_by(token=token).count())
            if auth_ok:
                user = User.query.filter_by(id=user_id).first()
                # return API key
                response = ({"user_name": user.user_name,
                             "user_id": user_id}, 201)
                logging.debug(f"Get User: {response=}")
                return response
            else:
                logging.exception("Get User: Authentication didn't work")
                return(({"status": "failure", "message": "Authentication didn't work"}), 400)
        except Exception as e:
            logging.exception(f"Get User: {e=}")
            return ({"message":  str(e)}, 400)

    def post(self):  # Register & login
        # has to have
        logging.info("Post User: Start")
        try:
            # data contains what is sent via the "body" argument in flutter.
            data = request.json
            logging.debug(f"Post User: {data=}")
            action = data.get("action")
            _email = str(data.get("email")).lower()
            username = data.get("user_name")
            password = data.get("password")
            if action == "register":
                logging.info("Post User: registering user")
                if User.query.filter_by(email=_email).count() > 0:
                    logging.exception(
                        f"Post User: E-Mail adress {_email} already in use.")
                    return(({"status": "failure", "message": "E-Mail adress already in use."}), 400)
                if User.query.filter_by(user_name=username).count() > 0:
                    logging.exception(
                        f"Post User: Username {username} already in use.")
                    return(({"status": "failure", "message": "Username already in use."}), 400)
                user = User(id=funcs.rand_user_id(), user_name=username, email=_email,
                            password=password,)
                # create user-exercises from admin exercises:

                db.session.add(user)
                db.session.commit()  # now the wo should have an id
                admin_user = User.query.filter_by(
                    user_name="kantnprojekt").first()
                ex_list = [Exercise.query.get(us_ex.exercise_id)
                           for us_ex in admin_user.exercises]
                for exercise in ex_list:
                    us_ex = UserExercise(
                        note=exercise.note,
                        exercise_id=exercise.id,
                        user_id=user.id,
                        user=user,
                        points=exercise.points,
                        max_points_day=exercise.max_points_day,
                        max_points_week=exercise.max_points_week,
                        daily_allowance=exercise.daily_allowance,
                        weekly_allowance=exercise.weekly_allowance,
                    )
                    db.session.add(us_ex)
                db.session.commit()  # now the wo should have an id
                response = (user.serialize(), 201)
                logging.debug(f"Post User: Registering: {response=}")
                return response
            elif action == "login":
                logging.info("Post User: user login")
                users = User.query.all()
                user = User.query.filter_by(
                    email=_email, password=password).first()
                if user is None:
                    if User.query.filter_by(email=_email).count() == 0:
                        logging.exception(f"Post User: Wrong email: {_email}")
                        return(({"status": "failure", "message": "Wrong email."}), 400)
                    else:
                        logging.exception(
                            f"Post User: Wrong password for {_email}")
                        return(({"status": "failure", "message": "Wrong password."}), 400)

                user.date_last_login = datetime.datetime.now()
                db.session.commit()
                response = (user.serialize(), 201)
                logging.debug(f"Post User: Login: {response=}")
                return response
            elif action == "reset_password":
                logging.info("Post User: reset password")
                old_password = data.get("old_password")
                if User.query.filter_by(email=_email, password=old_password).count() == 0:
                    if User.query.filter_by(email=_email).count() == 0:
                        logging.exception(f"Post User: Wrong email: {_email}")
                        return(({"status": "failure", "message": "Wrong email."}), 400)
                    else:
                        logging.exception(
                            f"Post User: Wrong password for {_email}")
                        return(({"status": "failure", "message": "Wrong password."}), 400)
                user = User.query.filter_by(
                    email=_email, password=old_password).first()
                # create new token, that means that all devices using the old token are automatically logged out as their token is not allowed anymore
                token = funcs.rand_string(30)
                user.password = password
                user.token = token
                db.session.commit()
                response = (user.serialize(), 201)
                logging.debug(f"Post User: Reset password: {response=}")
                return(response)
            else:
                logging.exception("Post User: Unknown User-request.")
                return(({"status": "failure", "message": "Unknown User-request."}), 400)
        except Exception as e:
            logging.exception(f"Post User: {e=}")
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self):
        pass
