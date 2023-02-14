import connexion
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import six
from fluigi_cloud.db.user import User

from fluigi_cloud.models.user_info_input import UserInfoInput  # noqa: E501
from fluigi_cloud.models.user_response import UserResponse  # noqa: E501
from fluigi_cloud import util


def get_user():  # noqa: E501
    """Get user information

    Get user information # noqa: E501


    :rtype: UserResponse
    """
    verify_jwt_in_request()
    print("JWT Identity:", get_jwt_identity())
    user_id = get_jwt_identity()
    workspace_ids = [str(workspace.id) for workspace in User.objects.get(id=user_id).workspaces]
    job_ids = [str(job.id) for job in User.objects.get(id=user_id).jobs]
    return {
        'user_id': user_id,
        'first_name': User.objects.get(id=user_id).first_name,
        'last_name': User.objects.get(id=user_id).last_name,
        'email': User.objects.get(id=user_id).email,
        'workspaces': workspace_ids,
        'jobs': job_ids
    }, 200


def update_user(body):  # noqa: E501
    """Update user information

    Update user information # noqa: E501

    :param body: Update user information
    :type body: dict | bytes

    :rtype: UserResponse
    """
    if connexion.request.is_json:
        body = UserInfoInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
