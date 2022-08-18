from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class User(Resource):
    
    @jwt_required
    def get(self, user_id:str):
        print("JWT Identity:", get_jwt_identity())
        return {'user_id': user_id}

    def put(self, user_id):
        return {'user_id': user_id}

    def delete(self, user_id):
        return {'user_id': user_id}
    
    
    