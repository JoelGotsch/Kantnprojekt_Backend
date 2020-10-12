from flask_restful import Resource
from flask import request, jsonify
from .models import User, db
import datetime
import random
from ..misc import funcs as funcs


class API_User(Resource):
    def get(self):  # To get usernames of other users
        # header = request.headers["Authorization"]
        # print(header)
        try:
            # email = request.args.get("email")
            token = request.headers.get("token")
            from_user_id = request.headers.get("user_id")
            # firebase_id_token=request.args.get("firebase_id_token")
            # verify the id token with firebase admin package! only then return api key.
            user_id = request.args.get("user_id")
            auth_ok = bool(User.query.filter_by(
                id=from_user_id, token=token).count())
            if auth_ok:
                user = User.query.filter_by(id=user_id).first()
                # return API key
                return(jsonify({"user_name": user.user_name, "user_id": user.id}), 201)
            else:
                return(({"status": "failure", "message": "Authentication didn't work"}), 400)
        except Exception as e:
            return jsonify({"message":  str(e)}, 400)

    def post(self):  # Register & login
        # has to have
        try:
            action = request.args.get("action")
            _email = str(request.args.get("email")).lower()
            password = request.args.get("password")
            if action == "register":
                if User.query.filter_by(email=_email).count() > 0:
                    return(({"status": "failure", "message": "E-Mail adress already in use."}), 400)
                user = User(username=request.args.get("user_name"), email=_email,
                            password=password,)
                db.session.add(user)
                db.session.commit()  # now the wo should have an id
                return(jsonify(user.serialize()), 201)
            elif action == "login":
                if User.query.filter_by(email=_email, password=password).count() == 0:
                    if User.query.filter_by(email=_email).count() == 0:
                        return(({"status": "failure", "message": "Wrong email."}), 400)
                    else:
                        return(({"status": "failure", "message": "Wrong password."}), 400)
                user = User.query.filter_by(
                    email=_email, password=password).first()
                user.date_last_login = datetime.datetime.now()
                db.session.commit()
                return(jsonify(user.serialize()), 201)
            elif action == "reset_password":
                old_password = request.args.get("old_password")
                if User.query.filter_by(email=_email, password=old_password).count() == 0:
                    if User.query.filter_by(email=_email).count() == 0:
                        return(({"status": "failure", "message": "Wrong email."}), 400)
                    else:
                        return(({"status": "failure", "message": "Wrong password."}), 400)
                user = User.query.filter_by(
                    email=_email, password=old_password).first()
                # create new token, that means that all devices using the old token are automatically logged out as their token is not allowed anymore
                token = funcs.rand_string(30)
                user.password = password
                user.token = token
                db.session.commit()
                return(jsonify(user.serialize()), 201)
            else:
                return(({"status": "failure", "message": "Unknown User-request."}), 400)
        except Exception as e:
            print(e)
            return(({"status": "failure", "message": "Could not read json or header."}), 400)

    def delete(self):
        pass
