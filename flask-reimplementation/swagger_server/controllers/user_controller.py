import connexion
import six

from swagger_server.models.user_info_input import UserInfoInput  # noqa: E501
from swagger_server.models.user_response import UserResponse  # noqa: E501
from swagger_server import util


def get_user():  # noqa: E501
    """Get user information

    Get user information # noqa: E501


    :rtype: UserResponse
    """
    return 'do some magic!'


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
