from flask import request
from flask_restful import Resource
from app.controllers.authentication import AuthenticationController

class Login(Resource):
    def post(self):
        body = request.get_json()
        if body is None:
            return {'error': 'Could not login, no input data recieved'}, 400
        return AuthenticationController.get_token(body)