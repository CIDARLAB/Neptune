import connexion
from flask import after_this_request, send_file
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import six
from app.controllers.authentication import AuthenticationController
from app.controllers.ziphelper import download_s3files_and_zip
from app.models.user import User
from app.models.workspace import Workspace

from fluigi_cloud.models.workspace_info_input import WorkspaceInfoInput  # noqa: E501
from fluigi_cloud.models.workspace_input import WorkspaceInput  # noqa: E501
from fluigi_cloud.models.workspace_response import WorkspaceResponse  # noqa: E501
from fluigi_cloud import util


def create_workspace(body):  # noqa: E501
    """create_workspace

    Create a workspace # noqa: E501

    :param body: Create a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInfoInput.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        name = body.workspace_name
        user_id = get_jwt_identity()
        workspace = Workspace(
            name=name,
        )
        workspace.save()
        user = User.objects.get(id=user_id)
        user.workspaces.append(workspace)
        user.save()
        return {'message': 'Workspace created successfully'}, 200


def delete_workspace(body):  # noqa: E501
    """delete_workspace

    Delete the workspace # noqa: E501

    :param body: Delete a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
        workspace_id = body.workspace_id
        verify_jwt_in_request()
        print("JWT Identity:", get_jwt_identity())
        user_id = get_jwt_identity()
        has_access = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
        
        if has_access == False:
            return {'message': 'User does not have access to this workspace'}, 401

        workspace = Workspace.objects.get(id=workspace_id)
        workspace.delete()
        return {'message': 'Workspace deleted successfully'}, 200


def get_workspace_zip_fs(body):  # noqa: E501
    """get_workspace_zip_fs

    Starts downloading the specified workspace as a zip file # noqa: E501

    :param body: Starts downloading the specified workspace
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
        workspace_id = body.workspace_id
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        AuthenticationController.check_user_workspace_access(user_id, workspace_id)
        workspace = Workspace.objects.get(id=workspace_id)

        # Run through all the files in the job and download them using the FileSystem APU
        files_list = [file.s3_path for file in workspace.design_files]

        # Zip the folder
        zip_file_name = download_s3files_and_zip(files_list)
        
        if zip_file_name is None:
            return {'message': 'Error downloading files'}, 500
        
        download_file_handle = open(zip_file_name, 'rb')

        @after_this_request
        def remove_file(response):
            try:
                download_file_handle.close()
                zip_file_name.unlink()
            except Exception as error:
                print("Error removing or closing downloaded file handle", error)
            return response

        return send_file(str(zip_file_name.absolute()), as_attachment=True, download_name=f'{workspace.name}.zip')

def get_workspaces(body):  # noqa: E501
    """get_workspaces

    Get all workspaces # noqa: E501

    :param body: Get all workspaces
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
        workspace_id = body.workspace_id
        verify_jwt_in_request()
        print("JWT Identity:", get_jwt_identity())
        user_id = get_jwt_identity()
        has_access = AuthenticationController.check_user_workspace_access(user_id, workspace_id)
        if has_access == False:
            return {'message': 'User does not have access to this workspace'}, 401
        
        workspace = Workspace.objects.get(id=workspace_id)
        return {
            'workspace_id': str(workspace.id),
            'name': workspace.name,
            'jobs': [str(job.id) for job in workspace.jobs],
            'design_files': [str(file.id) for file in workspace.design_files],
        }, 200


def update_workspace(body):  # noqa: E501
    """update_workspace

    Update the workspace # noqa: E501

    :param body: Update a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInfoInput.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        workspace_id = body.workspace_id
        workspace = Workspace.objects.get(id=workspace_id)
        workspace.name = body.workspace_name
        workspace.save()
        return {'message': 'Workspace updated successfully'}, 200
