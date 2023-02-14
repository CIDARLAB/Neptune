from pathlib import Path
import uuid
import connexion
from flask import send_file
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import six
from app.controllers.authentication import AuthenticationController
from app.controllers.s3filesystem import S3FileSystem
from app.controllers.workspace import add_new_file_to_workspace

from swagger_server.models.file_body import FileBody  # noqa: E501
from swagger_server.models.file_body1 import FileBody1  # noqa: E501
from swagger_server.models.file_body2 import FileBody2  # noqa: E501
from swagger_server.models.file_body3 import FileBody3  # noqa: E501
from swagger_server.models.file_copy_body import FileCopyBody  # noqa: E501
from swagger_server.models.file_fs_body import FileFsBody  # noqa: E501
from swagger_server.models.file_response import FileResponse  # noqa: E501
from swagger_server import util
from werkzeug.utils import secure_filename


def copy_file(body):  # noqa: E501
    """copy_file

    Copy a file to a specified workspace # noqa: E501

    :param body: Copy a file to a specified workspace
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileCopyBody.from_dict(connexion.request.get_json())  # noqa: E501
        file_id = body.file_id
        workspace_id = body.workspace_id

        verify_jwt_in_request()
        user_id = get_jwt_identity()
        AuthenticationController.check_user_file_access(user_id, file_id)
        AuthenticationController.check_user_workspace_access(user_id, workspace_id=workspace_id)

        file = File.objects.get(id=file_id)
        old_s3_path = file.s3_path
        new_s3_path = S3FileSystem.copy_file(old_s3_path)
        new_file = deepcopy(file)
        new_file.id = None
        new_file.s3_path = new_s3_path
        new_file.save()
        add_new_file_to_workspace(new_file, workspace_id)

        return {'message': 'File copied successfully', 'file_id': str(new_file.id)}, 200


def create_file(body):  # noqa: E501
    """Create a new file

    Create a new file # noqa: E501

    :param body: Create a new file
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody2.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        workspace_id = body.workspace_id
        file_name = body.file_name
        AuthenticationController.check_user_workspace_access(user_id, workspace_id=workspace_id)
        
        file = File(
            file_name=file_name,
            s3_path=S3FileSystem.create_new_file(file_name)
        )
        file.save()
        add_new_file_to_workspace(file, workspace_id)

        return file.to_json(), 200


def delete_file(body):  # noqa: E501
    """Delete a file

    Delete a file # noqa: E501

    :param body: Delete a file
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody3.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        file_id = body.file_id
        AuthenticationController.check_user_file_access(user_id, file_id)
        
        file = File.objects.get(id=file_id)
        # Delete linked s3 object
        s3path = file.s3_path
        S3FileSystem.delete_file(s3path)
        file.delete()
        file.save()
        return {'message': 'File deleted successfully'}, 200


def get_file(body):  # noqa: E501
    """Get file information

    Get file information # noqa: E501

    :param body: Get file information
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        file_id = body.file_id
        user_id = get_jwt_identity()
        AuthenticationController.check_user_file_access(user_id, file_id)
        
        file = File.objects.get(id=file_id)
        return file.to_json(), 200


def get_file_fs(body):  # noqa: E501
    """get_file_fs

    Starts downloading the specified file # noqa: E501

    :param body: Starts downloading the specified file
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = FileFsBody.from_dict(connexion.request.get_json())  # noqa: E501
        file_id = body.file_id
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        AuthenticationController.check_user_file_access(user_id, file_id)
        
        file = File.objects.get(id=file_id)
        file_name = file.file_name
        s3_path = file.s3_path

        file_download_path = Path(FLASK_DOWNLOADS_DIRECTORY)

        download_file_path = S3FileSystem.download_file(
            s3_location=s3_path, 
            download_location=file_download_path,
            preserve_s3_name=True
        )

        file_handle = open(download_file_path, 'rb')
        @after_this_request
        def remove_file(response):
            try:
                download_file_path.unlink()
                file_handle.close()
            except Exception as error:
                print("Error removing or closing downloaded file handle", error)
            return response
        
        return send_file(file_handle, as_attachment=True, download_name=file_name), 200


def post_file_fs(file, workspace_id):  # noqa: E501
    """post_file_fs

    Uploads a file to the specified workspace # noqa: E501

    :param file: 
    :type file: strstr
    :param workspace_id: 
    :type workspace_id: str

    :rtype: FileResponse
    """
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    
    if request is None:
        return {'message': 'Could not create file system, no input data recieved'}, 400
    workspace_id = request.form['workspace_id']

    # verify user has access to workspace
    is_authorized = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
    if is_authorized == False:
        return {'message': 'User does not have access to this workspace'}, 401
    
    uploaded_file = request.files['file']
    if uploaded_file.filename is None:
        return {'message': 'Could not create file system, no file recieved'}, 400
    filename = uploaded_file.filename
    
    if uploaded_file is None:
        return {'message': 'Could not create file system, no file recieved'}, 400
    upload_folder_filename = f'{uuid.uuid4()}-{secure_filename(filename)}'
    uploaded_file.save(upload_folder_filename)
    
    # Use the override file name so that if you want to upload a file but keep a different name
    s3_path = S3FileSystem.upload_file(Path(upload_folder_filename), override_file_name=filename)
    
    # Delete file from local storage
    Path(upload_folder_filename).unlink()

    # Create a new file object
    file = File(
        file_name=filename,
        s3_path=s3_path,
        file_extension=filename.split('.')[-1]
    )
    file.save()
    add_new_file_to_workspace(file, workspace_id)
    return {'message': 'File uploaded successfully'}, 200


def put_file_fs(file, workspace_id, file_id):  # noqa: E501
    """put_file_fs

    Uploads a file to the specified workspace replacing the existing file # noqa: E501

    :param file: 
    :type file: strstr
    :param workspace_id: 
    :type workspace_id: str
    :param file_id: 
    :type file_id: str

    :rtype: FileResponse
    """
    return 'do some magic!'


def update_file(body):  # noqa: E501
    """Update a file&#x27;s properties

    Update a file # noqa: E501

    :param body: Update a file
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody1.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        workspace_id = body.workspace_id
        file_name = body.file_name
        AuthenticationController.check_user_workspace_access(user_id, workspace_id=workspace_id)
        
        file = File(
            file_name=file_name,
            s3_path=S3FileSystem.create_new_file(file_name)
        )
        file.save()
        add_new_file_to_workspace(file, workspace_id)

        return file.to_json(), 200
