from flask import request
from flask_restful import Resource
from app.controllers.authentication import AuthenticationController

class Login(Resource):
    def post(self):
        body = request.get_json()
        if body is None:
            return {'error': 'Could not login, no input data recieved'}, 400
        
        email = body['email']
        password = body['password']
        if email is None or password is None:
            return {'error': 'Could not login, missing email or password'}, 400

        access_token = AuthenticationController.get_token(email=email, password=password)
        
        if access_token is None:
            return {'error': 'Could not login, invalid credentials'}, 400
        
        return {'message': 'User Authenticated Successfully','access_token': access_token}, 200
