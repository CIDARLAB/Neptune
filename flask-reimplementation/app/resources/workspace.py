from flask import request
from app.models.workspace import Workspace
from flask_restful import Resource

class WorkspaceAPI:
    
    class Base(Resource):
        def get(self, workspace_id):
            workspace = Workspace.objects.get(id=workspace_id)
            return workspace.to_json(), 200
        
        def delete(self):
            workspace_id = request.get_json()['workspace_id']
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.delete()
            return {'message': 'Workspace deleted successfully'}, 200
        
        def put(self):
            workspace_id = request.get_json()['workspace_id']
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.update(request.get_json())
            return {'message': 'Workspace updated successfully'}, 200
        
        def post(self):
            workspace_id = request.get_json()['workspace_id']
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.update(request.get_json())
            return {'message': 'Workspace updated successfully'}, 200
        
    class Zip(Resource):
        def get(self, workspace_id):
            workspace = Workspace.objects.get(id=workspace_id)
            return workspace.get_zip(), 200