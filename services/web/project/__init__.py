from flask import Blueprint, Flask
from flask_restful import Api
from .api_struc.models import db
from .api_struc.Test import Test
from .api_struc.Workout import API_Workout
from .api_struc.Exercise import API_Exercise
from .api_struc.User import API_User
from .api_struc.Challenge import API_Challenge, API_Challenges, API_ChallengeAccept
__version__ = "v0_2"

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# api.add_resource(Tasks, '/tasks')
api.add_resource(Test, "/test")
api.add_resource(API_Workout, "/workouts")
api.add_resource(API_Exercise, "/exercises")
api.add_resource(API_User, "/user")
api.add_resource(API_Challenge, "/challenge")
api.add_resource(API_Challenges, "/challenges")
api.add_resource(API_ChallengeAccept, "/challengeaccept")

# for testing: add /test in url-prefix and use configtest to use the kantnprojekt2 database instead!
app = Flask(__name__)

# app.config.from_object("project.config.Config")
app.config.from_object("project.configtest.Config")

db.init_app(app)
# handle migration via manage.py file!

# app.register_blueprint(api_bp, url_prefix='/'+str(__version__))
app.register_blueprint(api_bp, url_prefix='/test')
if __name__=="__main__":
    print("__init__.py was run now!!")