from flask import request
from flask_restful import Resource
from marshmallow import fields
from flask_apispec import use_kwargs
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.controllers.tasks import compile_lfr, compile_mint, test_task

class CompileAPI:
    
    class LFR(Resource):
        def post(self, **kwargs):
            body = request.get_json()
            if body is None:
                return {'error': 'Could not compile, no input data recieved'}, 400
            return compile_lfr(body)
        
    
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
            return str(result)