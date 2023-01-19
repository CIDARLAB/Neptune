from copy import deepcopy
from marshmallow import fields
from flask_apispec import use_kwargs
from app.controllers.s3filesystem import S3FileSystem
from app.controllers.workspace import add_new_file_to_workspace
from app.models.file import File
from flask_restful import Resource
from flask import request, send_file, after_this_request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.controllers.authentication import AuthenticationController
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from app.models.workspace import Workspace
from app.parameters import FLASK_DOWNLOADS_DIRECTORY

class FileAPI:
    class FileBase(Resource):

        @use_kwargs({
            'file_id': fields.Str(required=True),
        })
        def get(self, **kwargs):
            verify_jwt_in_request()
            file_id = kwargs.get('file_id')
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            return file.to_json(), 200
        
        @use_kwargs({'file_name': fields.Str(), 'workspace_id': fields.Str()})
        def post(self, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            workspace_id = kwargs.get('workspace_id')
            file_name = kwargs.get('file_name')
            AuthenticationController.check_user_workspace_access(user_id, workspace_id=workspace_id)
            
            file = File(
                file_name=file_name,
                s3_path=S3FileSystem.create_new_file(file_name)
            )
            file.save()
            add_new_file_to_workspace(file, workspace_id)

            return file.to_json(), 200
        
        @use_kwargs({
            'file_id': fields.Str(required=True),
        })
        def delete(self, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            file_id = kwargs.get('file_id')
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            # Delete linked s3 object
            s3path = file.s3_path
            S3FileSystem.delete_file(s3path)
            file.delete()
            file.save()
            return {'message': 'File deleted successfully'}, 200
        
        @use_kwargs({'file_id': fields.Str(),'payload': fields.Str()}) 
        def put(self, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            file_id = kwargs.get('file_id')
            AuthenticationController.check_user_file_access(user_id, file_id)
            payload = kwargs.get('payload')
            file = File.objects.get(id=file_id)
            s3path = file.s3_path
            S3FileSystem.update_file_content(s3path, payload)
            file.update()
            file.save()
            return {'message': 'File updated successfully'}, 200
        
    class FileCopy(Resource):
        @use_kwargs({'file_id': fields.Str(), 'workspace_id': fields.Str()})
        def post(self, **kwargs):
            if request is None:
                return {'error': 'Could not copy file, no input data recieved'}, 400
            file_id = kwargs.get('file_id')
            workspace_id = kwargs.get('workspace_id')

            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            AuthenticationController.check_user_workspace_access(user_id, workspace_id=workspace_id)

            file = File.objects.get(id=file_id)
            old_s3_path = file.s3_path
            new_s3_path = S3FileSystem.copy_file(old_s3_path)
            new_file = deepcopy(file)
            new_file.id = None
            new_file.s3_path = new_s3_path
            new_file.save()
            add_new_file_to_workspace(new_file, workspace_id)

            return {'message': 'File copied successfully', 'file_id': str(new_file.id)}, 200
        
    class FileSystem(Resource):

        @use_kwargs({'file_id': fields.Str()})
        def get(self, **kwargs):
            file_id = kwargs.get('file_id')
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_file_access(user_id, file_id)
            
            file = File.objects.get(id=file_id)
            file_name = file.file_name
            s3_path = file.s3_path

            file_download_path = Path(FLASK_DOWNLOADS_DIRECTORY)

            download_file_path = S3FileSystem.download_file(
                s3_location=s3_path, 
                download_location=file_download_path,
                preserve_s3_name=True
            )

            file_handle = open(download_file_path, 'rb')
            @after_this_request
            def remove_file(response):
                try:
                    download_file_path.unlink()
                    file_handle.close()
                except Exception as error:
                    print("Error removing or closing downloaded file handle", error)
                return response
            
            return send_file(file_handle, as_attachment=True, download_name=file_name), 200
        
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
            upload_folder_filename = f'{uuid.uuid4()}-{secure_filename(filename)}'
            uploaded_file.save(upload_folder_filename)
            
            # Use the override file name so that if you want to upload a file but keep a different name
            s3_path = S3FileSystem.upload_file(Path(upload_folder_filename), override_file_name=filename)
            
            # Delete file from local storage
            Path(upload_folder_filename).unlink()

            # Create a new file object
            file = File(
                file_name=filename,
                s3_path=s3_path,
                file_extension=filename.split('.')[-1]
            )
            file.save()
            add_new_file_to_workspace(file, workspace_id)
            return {'message': 'File uploaded successfully'}, 200
