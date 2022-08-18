from flask_restful import Resource
from app.models.user import User
from flask import request

class Signup(Resource):
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        # TODO- Find a more elegant way to do this
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            return {"msg": "User already exists"}, 400

        new_user = User(email=email, password=password)
        new_user.hash_password()
        new_user.save()
        
        return {"msg": "User created successfully", "user_id": str(new_user.id)}, 200
    