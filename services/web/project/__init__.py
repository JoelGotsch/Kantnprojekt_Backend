from flask import Blueprint, Flask
from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
from .api_struc.models import db
from .api_struc.Test import Test
from .api_struc.Workout import API_Workout
from .api_struc.Exercise import API_Exercise
# from code.API import db, Test

__version__ = "v0_1"

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# api.add_resource(Tasks, '/tasks')
api.add_resource(Test, "/test")
api.add_resource(API_Workout, "/workouts")
api.add_resource(API_Exercise, "/exercises")

app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)
# db = SQLAlchemy(app)

app.register_blueprint(api_bp, url_prefix='/'+str(__version__))

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_object(config_filename)
#     app.register_blueprint(api_bp, url_prefix='/api/'+str(__version__))
#     db.init_app(app)

#     return(app, db)


# app, db = create_app("config")
# # app.run() # has to be run by 
# # if __name__ == "__main__":
# #    #actually, this should change and use the .env or .env.prod 
# #   app, db = create_app("config")
# #   app.run(debug=True,host="127.0.0.1", port=8002)

if __name__=="__main__":
    print("__init__.py was run now!!")