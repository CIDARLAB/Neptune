from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserAPI(Resource):
    
    @jwt_required
    def get(self):
        print("JWT Identity:", get_jwt_identity())
        return {'email_id': get_jwt_identity()}
