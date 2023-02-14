from pathlib import Path
import connexion
import six
from app.controllers.authentication import AuthenticationController
from app.controllers.s3filesystem import S3FileSystem
from app.models.file import File
from app.models.user import User
from app.models.workspace import Workspace

from fluigi_cloud.models.login_input import LoginInput  # noqa: E501
from fluigi_cloud.models.register_input import RegisterInput  # noqa: E501
from fluigi_cloud.models.update_password_input import UpdatePasswordInput  # noqa: E501
from fluigi_cloud.models.user_response import UserResponse  # noqa: E501
from fluigi_cloud import util


def change_password(body):  # noqa: E501
    """Change password

    Change password # noqa: E501

    :param body: Change password
    :type body: dict | bytes

    :rtype: UserResponse
    """
    if connexion.request.is_json:
        body = UpdatePasswordInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_user(body):  # noqa: E501
    """Login a user

    Login a user # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: UserResponse
    """
    if connexion.request.is_json:
        body = LoginInput.from_dict(connexion.request.get_json())  # noqa: E501
        
        email = body.email
        password = body.password
        if email is None or password is None:
            return {'error': 'Could not login, missing email or password'}, 400

        access_token = AuthenticationController.get_token(email=email, password=password)
        
        if access_token is None:
            return {'error': 'Could not login, invalid credentials'}, 400
        
        return {'message': 'User Authenticated Successfully','access_token': access_token}, 200


def register_user(body):  # noqa: E501
    """Register a new user

    Register a new user # noqa: E501

    :param body: Register a new user
    :type body: dict | bytes

    :rtype: UserResponse
    """
    if connexion.request.is_json:
        body = RegisterInput.from_dict(connexion.request.get_json())  # noqa: E501
        
        email = body.email
        password = body.password

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
    