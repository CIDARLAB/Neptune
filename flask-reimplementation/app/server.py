from flask import Blueprint, Flask
from flask_restful import Api
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import mongoengine
from app.parameters import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_NEPTUNE_DB,
    MONGODB_USER,
    MONGODB_PASSWORD
)

# Setting up the basic blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)
# Adding the resources
# TODO - do the thing


path =   os.path.abspath("./static/")
print(path)
flask_app = Flask(__name__, static_folder=path)

# Registering the blueprint
flask_app.register_blueprint(api_blueprint)

# Do the bcrypt thing
bcrypt = Bcrypt(flask_app)
flask_app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
flask_app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
flask_app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(flask_app)



# Importing the resources

# Serve the static files
@flask_app.route('/')
def index():
    return flask_app.send_static_file('index.html')


def connect_to_mongodb():
    print("Connecting to MongoDB")
    mongoengine.connect(
        db=MONGO_NEPTUNE_DB,
        host=MONGO_HOST,
        port=MONGO_PORT,
        username=MONGODB_USER,
        password=MONGODB_PASSWORD
    )

def connect_to_redis():
    print("Connecting to Redis")
    
def connect_to_s3():
    print("Connecting to S3")
    
def connect_to_celery():
    print("Connecting to Celery")
    
def setup_socketio(flask_app):
    print("Setting up SocketIO")

if __name__ == "__main__":
    connect_to_mongodb()
    connect_to_celery()
    connect_to_redis()
    setup_socketio(flask_app)
    # Run the app
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
    