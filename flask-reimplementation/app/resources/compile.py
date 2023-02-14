from flask import request
from flask_restful import Resource
from marshmallow import fields
from flask_apispec import use_kwargs
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.file import File

from app.controllers.tasks import dispatch_compile_lfr, compile_mint, test_task

class CompileAPI:
    
    class LFR(Resource):
        @use_kwargs({
            'source_files': fields.List(fields.Str()), 
            'config_file': fields.Str(), 
            'args': fields.List(fields.Str())
        })
        def post(self, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            source_file_ids = kwargs.get('source_files')
            config_file_id = kwargs.get('config_file')
            args = kwargs.get('args')
            
            source_files = [File.objects.get(id=file_id) for file_id in source_file_ids]
            config_file = File.objects.get(id=config_file_id)
            if args is None:
                args = []
            result = dispatch_compile_lfr(user_id, source_files, config_file, args)
            return 
        
    
    class MINT(Resource):
        def post(self, **kwargs):
            body = request.get_json()
            if body is None:
                return {'error': 'Could not compile, no input data recieved'}, 400
            return compile_mint(body)

    class TestTask(Resource):
        @use_kwargs({'x': fields.Int(), 'y': fields.Int()})
        def post(self, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            x = kwargs.get('x')
            y = kwargs.get('y')
            result = test_task(user_id, x, y)
            return {"job_id": str(result.id)}, 200