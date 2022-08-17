from flask import Blueprint, Flask
from flask_restful import Api
import os

# Setting up the basic blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

path =   os.path.abspath("./static/")
print(path)
flask_app = Flask(__name__, static_folder=path)

# Importing the resources

# Serve the static files
@flask_app.route('/')
def index():
    return flask_app.send_static_file('index.html')

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
    