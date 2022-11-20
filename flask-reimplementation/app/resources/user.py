from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

class UserAPI(Resource):
    
    def get(self):
        verify_jwt_in_request()
        print("JWT Identity:", get_jwt_identity())
        user_id = get_jwt_identity()
        return {'user_id': user_id}, 200
