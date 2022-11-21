from app.controllers.filesystem import FileSystem
from app.models.file import File
from flask_restful import Resource
from flask import request, send_file
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.controllers.authentication import AuthenticationController
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from app.models.workspace import Workspace

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
            file_name = file.file_name
            s3_path = file.s3_path
            FileSystem.download_file(file_name, s3_path, preserve_s3_name=True)

            return send_file(s3_path, as_attachment=True, download_name=file_name), 200
        
        def post(self):
            
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            if request is None:
                return {'message': 'Could not create file system, no input data recieved'}, 400
            workspace_id = request.form['workspace_id']

            # verify user has access to workspace
            is_authorized = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
            if is_authorized == False:
                return {'message': 'User does not have access to this workspace'}, 401
            
            uploaded_file = request.files['file']
            if uploaded_file.filename is None:
                return {'message': 'Could not create file system, no file recieved'}, 400
            filename = uploaded_file.filename
            
            if uploaded_file is None:
                return {'message': 'Could not create file system, no file recieved'}, 400
            upload_foler_filename = f'{uuid.uuid4()}-{secure_filename(filename)}'
            uploaded_file.save(upload_foler_filename)
            
            s3_path = FileSystem.upload_file(Path(upload_foler_filename), override_file_name=filename)
            
            # Delete file from local storage
            Path(upload_foler_filename).unlink()

            # Create a new file object
            file = File(
                file_name=filename,
                s3_path=s3_path,
                file_extension=filename.split('.')[-1]
            )
            file.save()
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.design_files.append(file)
            workspace.save()
            return {'message': 'File uploaded successfully'}, 200
