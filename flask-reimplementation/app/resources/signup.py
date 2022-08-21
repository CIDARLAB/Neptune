from pathlib import Path
from flask_restful import Resource
from app.models.user import User
from app.models.workspace import Workspace
from app.models.file import File
from app.controllers.filesystem import FileSystem
from flask import request
import os

class Signup(Resource):
    def post(self):
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

        new_user = User(email=email, password=password)
        new_user.hash_password()
        
        # Create a new workspace called "Microfluidics Examples"
        new_workspace = Workspace(name="Microfluidics Examples")
        
        # Step 1 - Go through every file in the examples directory 
        # Step 2 - Upload these files to s3 and get the file_id
        # Step 3 - Create a new file object for each of the file_ids and add it to the workspace
        
        # Go through every file in the examples directory
        examples_directory = Path("examples")
        for file_name in examples_directory.iterdir():
            # Upload the file to s3 and get the file_id
            s3_object_id = FileSystem.upload_file(file_name)
            
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
        
        return {"msg": "User created successfully", "user_id": str(new_user.id)}, 200
    