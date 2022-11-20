from flask import Blueprint, Flask, jsonify, send_from_directory
from flask_restful import Api
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import mongoengine
from app.controllers.filesystem import FileSystem
from app.parameters import (
    MONGO_HOST,
    MONGO_PORT,
    NEPTUNE_MONGODB_DBNAME,
    MONGODB_USER,
    MONGODB_PASSWORD
)
from app.resources.file import FileAPI
from app.resources.login import Login
from app.resources.signup import Signup
from app.resources.workspace import WorkspaceAPI
from app.resources.user import UserAPI
from app.resources.job import JobAPI
from app.resources.compile import CompileAPI

# Setting up the basic blueprint
api_blueprint = Blueprint('api', __name__, )
api = Api(api_blueprint)

# Adding the resources
api.add_resource(Signup,'/api/v2/register')
api.add_resource(Login,'/api/v2/login')
api.add_resource(FileAPI.FileBase, '/api/v2/file/<string:file_id>')
api.add_resource(FileAPI.FileCopy, '/api/v2/file/copy')
api.add_resource(FileAPI.FileFileSystem, '/api/v2/file/fs')
api.add_resource(WorkspaceAPI.WorkspaceBase, '/api/v2/workspace')
api.add_resource(WorkspaceAPI.WorkspaceZip, '/api/v2/workspace/zipfs')
api.add_resource(JobAPI.JobBase, '/api/v2/job')
api.add_resource(JobAPI.JobZip, '/api/v2/job/zipfs')
api.add_resource(CompileAPI.LFR, '/api/v2/compile/lfr')
api.add_resource(CompileAPI.MINT, '/api/v2/compile/mint')
api.add_resource(UserAPI, '/api/v2/user')


path =   os.path.abspath("./static/")
print(path)
flask_app = Flask(__name__, static_url_path="/", static_folder=path)
CORS(flask_app)

# Registering the blueprint
flask_app.register_blueprint(api_blueprint)

# Do the bcrypt thing
bcrypt = Bcrypt(flask_app)
flask_app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
flask_app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
flask_app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(flask_app)


# Serve the static files
@flask_app.route('/')
def index():
    return flask_app.send_static_file('index.html')


@flask_app.route('/echo/<input_string>')
def echo(input_string: str) :
    '''
    Simple call and response API Function
    '''
    return jsonify(
        {
            "Input String": f'{input_string}'
        }
    )


def connect_to_mongodb():
    print("Connecting to MongoDB")
    mongoengine.connect(
        db=NEPTUNE_MONGODB_DBNAME,
        host=MONGO_HOST,
        port=MONGO_PORT,
        username=MONGODB_USER,
        password=MONGODB_PASSWORD
    )

def connect_to_redis():
    # print("Connecting to Redis")
    pass
    
def connect_to_s3():
    # Check if s3 connection is working
    is_connected = FileSystem.test_connection()
    if not is_connected:
        print("S3 Connection Failed")
    pass
    
def connect_to_celery():
    # print("Connecting to Celery")
    pass
    
def setup_socketio(flask_app):
    # print("Setting up SocketIO")
    pass


connect_to_mongodb()
connect_to_s3()

if __name__ == "__main__":
    connect_to_mongodb()
    connect_to_s3()
    connect_to_celery()
    connect_to_redis()
    setup_socketio(flask_app)
    # Run the app
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
    