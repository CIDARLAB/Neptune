from pathlib import Path
from flask_restful import Resource
from app.controllers.authentication import AuthenticationController
from fluigi_cloud.db.user import User
from fluigi_cloud.db.workspace import Workspace
from fluigi_cloud.db.file import File
from app.controllers.s3filesystem import S3FileSystem
from flask import request
from marshmallow import fields
from flask_apispec import use_kwargs

class Signup(Resource):

    @use_kwargs({'email': fields.Str(), 'password': fields.Str()})
    def post(self, **kwargs):

        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        # TODO- Find a more elegant way to do this
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            return {"msg": "User already exists"}, 400

        request_body = request.get_json()
        if request_body is None:
            return {'error': 'Could not create user, no input data recieved'}, 400

        email=request_body['email'],
        password=request_body['password'],
        first_name=request_body['first_name'] if 'first_name' in request_body else None,
        last_name=request_body['last_name'] if 'last_name' in request_body else None,

        new_user = AuthenticationController.create_new_user(
            email=email[0], 
            password=password[0], 
            first_name=first_name[0] if first_name else None,
            last_name=last_name[0] if last_name else None
        )
        
        # Create a new workspace called "Microfluidics Examples"
        new_workspace = Workspace(name="Microfluidics Examples")
        
        # Step 1 - Go through every file in the examples directory 
        # Step 2 - Upload these files to s3 and get the file_id
        # Step 3 - Create a new file object for each of the file_ids and add it to the workspace
        
        # Go through every file in the examples directory
        examples_directory = Path("examples")
        for file_name in examples_directory.iterdir():
            # Upload the file to s3 and get the file_id
            s3_object_id = S3FileSystem.upload_file(file_name)
            
            # Create a new file object for the file_id and add it to the workspace
            new_file = File(file_name=str(file_name.name), s3_path=s3_object_id)
            new_file.save()
            new_workspace.design_files.append(new_file)
        
        # Save the workspace
        new_workspace.save()
        
        # Add the workspace to the user
        new_user.workspaces.append(new_workspace)
        
        # Save the user        
        new_user.save()

        auth_message, return_code, access_token = AuthenticationController.get_token(email=email[0], password=password[0])

        if access_token is None:
            return {'message': auth_message}, return_code
        
        return {'message': f'Created a new user successfully! {auth_message}', 'access_token': access_token}, 200
    