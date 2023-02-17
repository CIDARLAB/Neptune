#!/usr/bin/env python3

import connexion

import encoder



import asyncio
import pathlib
from flask import jsonify
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import mongoengine
from app.controllers.s3filesystem import S3FileSystem
from fluigi_cloud.parameters import (
    FLASK_DOWNLOADS_DIRECTORY,
    MONGO_HOST,
    MONGO_PORT,
    NEPTUNE_MONGODB_DBNAME,
    MONGODB_USER,
    MONGODB_PASSWORD,
    FLASK_UPLOADS_DIRECTORY
)
from flask_socketio import SocketIO







def setup_fileio_directories():
    print("Setting up FileIO Directories")
    try:
        # Check if the uploads directory exists and create if they don't
        pathlib.Path(FLASK_UPLOADS_DIRECTORY).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating uploads directory: {e}")

    try:
        # Check if downloads directory exists and create if they don't
        pathlib.Path(FLASK_DOWNLOADS_DIRECTORY).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating downloads directory: {e}")
    
    print("FileIO Directories Setup Complete")

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
    is_connected = S3FileSystem.test_connection()
    if not is_connected:
        print("S3 Connection Failed")
    pass
    
def connect_to_celery():
    # print("Connecting to Celery")
    pass
    
def setup_socketio(flask_app):
    # print("Setting up SocketIO")
    pass
    

setup_fileio_directories()
connect_to_mongodb()
connect_to_s3()
connect_to_celery()
connect_to_redis()
path = os.path.abspath("../static/")

# This is the openapi spec driven server
flask_app = connexion.FlaskApp(__name__, specification_dir='./swagger/', server_args={'static_url_path':"/", 'static_folder':path})  #static_url_path="/", static_folder=path
flask_app.app.json_provider_class = encoder.JSONEncoder
flask_app.add_api('swagger.yaml', arguments={'title': 'Neptune API'}, pythonic_params=True)
CORS(flask_app.app)
flask_app.app.config['UPLOAD_FOLDER'] = FLASK_UPLOADS_DIRECTORY
# Do the bcrypt thing
bcrypt = Bcrypt(flask_app.app)
flask_app.app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
flask_app.app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
flask_app.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
flask_app.app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(flask_app.app)

# Setting up callback event loop for async io
# This will basically use the asyncio for compile 
# job completion document updates
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Setup the Socketio bits now
socketio = SocketIO(flask_app.app, cors_allowed_origins="*")
setup_socketio(flask_app.app)

# Test Event to ensure things are working correctly
@socketio.on('echo')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    socketio.emit('echo', json)


@socketio.on('connection')
def handle_connection():
    print("A new SocketIO Connection Established")


@socketio.on('monitor')
def handle_monitor(job_id):
    print(f"Received a monitor request for job: {job_id}")
    #socketio.join('monitor', job_id)
    # Check if the job exists and join the room using the job_id
    pass


# Serve the static files
@flask_app.app.route('/')
def index():
    return flask_app.app.send_static_file('index.html')

# Serve the socketio test page
@flask_app.app.route('/test/socketio')
def test_socketio():
    return flask_app.send_static_file('socket.html')


# Flask Routes
@flask_app.app.route('/echo/<input_string>')
def echo(input_string: str) :
    '''
    Simple call and response API Function
    '''
    return jsonify(
        {
            "Input String": f'{input_string}'
        }
    )

# if __name__ == '__main__':
    # Run the app
socketio.run(flask_app.app, debug=True, host="0.0.0.0", port=8080)

