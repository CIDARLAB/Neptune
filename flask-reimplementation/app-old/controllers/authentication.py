from typing import Optional, Tuple, Dict
from app.models.user import User
import datetime
from flask_jwt_extended import create_access_token

class AuthenticationController:
    
    @staticmethod
    def create_new_user(email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        """ Creates a new user in the database

        Args:
            email (str): The email of the user
            password (str): The password of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user

        Returns:
            _type_: The newly created user document object
        """
        # Create a new user
        user = User(
            email=email,
            password=password,
            first_name=first_name if first_name else "",
            last_name=last_name if last_name else "",
            created_at=datetime.datetime.utcnow()
        )
        user.hash_password()
        user.save()
        return user
    
    @staticmethod
    def get_token(email: str, password: str) -> Tuple[str, int, Optional[str]]:
        """Generates the token for given user

        Args:
            email (str): the email of the user
            password (str): the password provided by the user

        Returns:
            Tuple[str, int, Optional[str]]: the message, the status code and an optional access token
        """        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 'Error: Unknown User', 401, None
        is_authorized = user.check_password(password)
        
        if not is_authorized:
            return 'Error: Invalid credentials', 401, None
        
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        
        return 'Successfully generated auth token', 200, access_token
    
    @staticmethod
    def update_password(old_password: str, new_password: str, email: str) -> Tuple[str, int]:
        """Updates the password of the user

        Args:
            old_password (str): the old password of the user
            new_password (str): the new password of the user
            email (str): the email of the user

        Returns:
            Tuple[str, int]: the message and the status code
        """        
        user = User.objects.get(email)
        if not user.check_password(old_password):
            return 'Invalid credentials', 401
        user.password = new_password
        user.hash_password()
        user.save()
        return 'Password updated successfully', 201
    
    
    @staticmethod
    def check_user_workspace_access(user_id: str, workspace_id: str) -> bool:
        """Checks if the user has access to the workspace

        Args:
            user_id (str): the id of the user
            workspace_id (str): the id of the workspace

        Returns:
            bool: True if the user has access to the workspace, False otherwise
        """        
        user = User.objects.get(id=user_id)
        for workspace in user.workspaces:
            if str(workspace.id) == workspace_id:
                return True
        return False

    @staticmethod
    def check_user_job_access(user_id: str, job_id: str) -> bool:
        """Checks if the user has access to the job

        Args:
            user_id (str): the id of the user
            job_id (str): the id of the job

        Returns:
            bool: True if the user has access to the job, False otherwise
        """        
        user = User.objects.get(id=user_id)
        for job in user.jobs:
            if str(job.id) == job_id:
                return True
        return False
    
    @staticmethod
    def check_user_file_access(user_id: str, file_id: str) -> bool:
        """Checks if the user has access to the file

        Args:
            user_id (str): the id of the user
            file_id (str): the id of the file

        Returns:
            bool: True if the user has access to the file, False otherwise
        """        
        user = User.objects.get(id=user_id)
        for workspace in user.workspaces:
            for file in workspace.files:
                if str(file.id) == file_id:
                    return True
        return False