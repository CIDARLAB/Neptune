from pathlib import Path
import uuid
from flask import request
from app.controllers.authentication import AuthenticationController
from app.controllers.ziphelper import download_s3files_and_zip
from app.models.workspace import Workspace
from flask_restful import Resource
from marshmallow import fields
from flask_apispec import use_kwargs
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import request, send_file, after_this_request

from app.parameters import FLASK_DOWNLOADS_DIRECTORY

class WorkspaceAPI:
    
    class WorkspaceBase(Resource):
        
        @use_kwargs({'workspace_id': fields.Str()})
        def get(self, **kwargs):
            workspace_id = kwargs.get('workspace_id')
            verify_jwt_in_request()
            print("JWT Identity:", get_jwt_identity())
            user_id = get_jwt_identity()
            has_access = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
            if has_access == False:
                return {'message': 'User does not have access to this workspace'}, 401
            
            workspace = Workspace.objects.get(id=workspace_id)
            return {
                'workspace_id': str(workspace.id),
                'name': workspace.name,
                'jobs': [str(job.id) for job in workspace.jobs],
                'design_files': [str(file.id) for file in workspace.design_files],
            }, 200
        
        @use_kwargs({'workspace_id': fields.Str()})
        def delete(self, **kwargs):
            workspace_id = kwargs.get('workspace_id')
            verify_jwt_in_request()
            print("JWT Identity:", get_jwt_identity())
            user_id = get_jwt_identity()
            has_access = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
            
            if has_access == False:
                return {'message': 'User does not have access to this workspace'}, 401

            workspace = Workspace.objects.get(id=workspace_id)
            workspace.delete()
            return {'message': 'Workspace deleted successfully'}, 200
        
        @use_kwargs({'workspace_id': fields.Str()})
        def put(self, **kwargs):
            verify_jwt_in_request()
            workspace_id = kwargs.get('workspace_id')
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.update(request.get_json())
            return {'message': 'Workspace updated successfully'}, 200
                
                
        @use_kwargs({'workspace_name': fields.Str()})
        def post(self, **kwargs):
            verify_jwt_in_request()
            name = kwargs.get('workspace_name')
            user_id = get_jwt_identity()
            workspace = Workspace(
                name=name,
            )
            workspace.save()
            user = User.objects.get(id=user_id)
            user.workspaces.append(workspace)
            user.save()
            return {'message': 'Workspace created successfully'}, 200
        
    class WorkspaceZip(Resource):
        
        @use_kwargs({'workspace_id': fields.Str()})
        def get(self, **kwargs):
            workspace_id = kwargs.get('workspace_id')
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            AuthenticationController.check_user_workspace_access(user_id, workspace_id)
            workspace = Workspace.objects.get(id=workspace_id)

            # Run through all the files in the job and download them using the FileSystem APU
            files_list = [file.s3_path for file in workspace.design_files]

            # Zip the folder
            zip_file_name = download_s3files_and_zip(files_list)
            
            download_file_handle = open(zip_file_name, 'rb')

            @after_this_request
            def remove_file(response):
                try:
                    download_file_handle.close()
                    zip_file_name.unlink()
                except Exception as error:
                    print("Error removing or closing downloaded file handle", error)
                return response

            return send_file(str(zip_file_name.absolute()), as_attachment=True, download_name=f'{workspace.name}.zip')