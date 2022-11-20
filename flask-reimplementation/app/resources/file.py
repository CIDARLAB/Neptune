from app.models.file import File
from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.controllers.authentication import AuthenticationController

class FileAPI:
    class FileBase(Resource):
        def get(self, file_id):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            return file.to_json(), 200
        
        def delete(self, file_id):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            file.delete()
            return {'message': 'File deleted successfully'}, 200
        
        def put(self, file_id):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            file.update(request.get_json()['payload'])
            return {'message': 'File updated successfully'}, 200
        
    class FileCopy(Resource):
        def post(self):
            if request is None:
                return {'error': 'Could not copy file, no input data recieved'}, 400
            file_id = request.get_json()['file_id']
            
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)

            file = File.objects.get(id=file_id)
            new_file = file.copy()
            return {'message': 'File copied successfully', 'file_id': str(new_file.id)}, 200
        
    class FileSystem(Resource):
        def get(self, file_id):
            
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            return file.get_file_systems(), 200
        
        def post(self):
            if request is None:
                return {'error': 'Could not create file system, no input data recieved'}, 400
            
            file_id = request.get_json()['file_id']
            file_system_id = request.get_json()['file_system_id']
            file = File.objects.get(id=file_id)
            file.add_file_system(file_system_id)
            return {'message': 'File added successfully'}, 200