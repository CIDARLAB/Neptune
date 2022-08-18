from app.models.file import File
from flask_restful import Resource
from flask import request

class FileAPI(Resource):
    def get(self, file_id):
        file = File.objects.get(id=file_id)
        return file.to_json(), 200
    
    def delete(self):
        file_id = request.get_json()['file_id']
        file = File.objects.get(id=file_id)
        file.delete()
        return {'message': 'File deleted successfully'}, 200
    
    def put(self):
        file_id= request.get_json()['file_id']
        file = File.objects.get(id=file_id)
        file.update(request.get_json())
        return {'message': 'File updated successfully'}, 200
    
    def post(self):
        file_id = request.get_json()['file_id']
        file = File.objects.get(id=file_id)
        file.update(request.get_json())
        return {'message': 'File updated successfully'}, 200