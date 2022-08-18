from app.models.user import User
import datetime
from flask_jwt_extended import create_access_token

class AuthenticationController:
    
    def create_new_user(request):
        # Create a new user
        pass
        
    def get_token(request_body):
        user = User.objects.get(email=request_body['email'])
        is_authorized = user.check_password(request_body['password'])
        
        if not is_authorized:
            return {'error': 'Invalid credentials'}, 401
        
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.user_id), expires_delta=expires)
        
        return {'token': access_token, 'user_id': user.user_id}, 200
    
    def update_password(request_body):
        
        # Update the password of a user
        user = User.objects.get(email=request_body['email'])
        user.password = request_body['password']
        return {'message': 'Password updated successfully'}, 201
    
        