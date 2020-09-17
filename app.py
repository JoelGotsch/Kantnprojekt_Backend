from flask import Blueprint, Flask
from flask_restful import Api
from resources.Register import Register
from resources.Signin import Signin
from resources.task import Tasks
from resources.Test import Test

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
__version__ = "v0_1"
# api.add_resource(Tasks, '/tasks')
api.add_resource(Test, "/test")

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api/'+str(__version__))

    from models import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True,host="127.0.0.1", port=8001)