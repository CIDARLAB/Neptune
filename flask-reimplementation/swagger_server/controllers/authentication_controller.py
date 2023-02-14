import connexion
import six

from swagger_server.models.login_input import LoginInput  # noqa: E501
from swagger_server.models.register_input import RegisterInput  # noqa: E501
from swagger_server.models.update_password_input import UpdatePasswordInput  # noqa: E501
from swagger_server.models.user_response import UserResponse  # noqa: E501
from swagger_server import util


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
    return 'do some magic!'


def register_user(body):  # noqa: E501
    """Register a new user

    Register a new user # noqa: E501

    :param body: Register a new user
    :type body: dict | bytes

    :rtype: UserResponse
    """
    if connexion.request.is_json:
        body = RegisterInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
