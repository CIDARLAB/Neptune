import connexion
import six

from swagger_server.models.workspace_info_input import WorkspaceInfoInput  # noqa: E501
from swagger_server.models.workspace_input import WorkspaceInput  # noqa: E501
from swagger_server.models.workspace_response import WorkspaceResponse  # noqa: E501
from swagger_server import util


def create_workspace(body):  # noqa: E501
    """create_workspace

    Create a workspace # noqa: E501

    :param body: Create a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInfoInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_workspace(body):  # noqa: E501
    """delete_workspace

    Delete the workspace # noqa: E501

    :param body: Delete a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_workspace_zip_fs(body):  # noqa: E501
    """get_workspace_zip_fs

    Starts downloading the specified workspace as a zip file # noqa: E501

    :param body: Starts downloading the specified workspace
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_workspaces(body):  # noqa: E501
    """get_workspaces

    Get all workspaces # noqa: E501

    :param body: Get all workspaces
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_workspace(body):  # noqa: E501
    """update_workspace

    Update the workspace # noqa: E501

    :param body: Update a workspace
    :type body: dict | bytes

    :rtype: WorkspaceResponse
    """
    if connexion.request.is_json:
        body = WorkspaceInfoInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
