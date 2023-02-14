import connexion
import six

from swagger_server.models.file_body import FileBody  # noqa: E501
from swagger_server.models.file_body1 import FileBody1  # noqa: E501
from swagger_server.models.file_body2 import FileBody2  # noqa: E501
from swagger_server.models.file_body3 import FileBody3  # noqa: E501
from swagger_server.models.file_copy_body import FileCopyBody  # noqa: E501
from swagger_server.models.file_fs_body import FileFsBody  # noqa: E501
from swagger_server.models.file_response import FileResponse  # noqa: E501
from swagger_server import util


def copy_file(body):  # noqa: E501
    """copy_file

    Copy a file to a specified workspace # noqa: E501

    :param body: Copy a file to a specified workspace
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileCopyBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_file(body):  # noqa: E501
    """Create a new file

    Create a new file # noqa: E501

    :param body: Create a new file
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody2.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_file(body):  # noqa: E501
    """Delete a file

    Delete a file # noqa: E501

    :param body: Delete a file
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody3.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_file(body):  # noqa: E501
    """Get file information

    Get file information # noqa: E501

    :param body: Get file information
    :type body: dict | bytes

    :rtype: FileResponse
    """
    if connexion.request.is_json:
        body = FileBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_file_fs(body):  # noqa: E501
    """get_file_fs

    Starts downloading the specified file # noqa: E501

    :param body: Starts downloading the specified file
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = FileFsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_file_fs(file, workspace_id):  # noqa: E501
    """post_file_fs

    Uploads a file to the specified workspace # noqa: E501

    :param file: 
    :type file: strstr
    :param workspace_id: 
    :type workspace_id: str

    :rtype: FileResponse
    """
    return 'do some magic!'


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
    return 'do some magic!'
