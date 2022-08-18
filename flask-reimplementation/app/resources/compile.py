from flask import request

class CompileAPI:
    
    class LFR(Resource):
        def post(self):
            body = request.get_json()
            if body is None:
                return {'error': 'Could not compile, no input data recieved'}, 400
            return compile_lfr(body)
        
    
    class MINT(Resource):
        def post(self):
            body = request.get_json()
            if body is None:
                return {'error': 'Could not compile, no input data recieved'}, 400
            return compile_mint(body)