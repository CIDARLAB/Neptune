# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserInfoInput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, user_id: str=None, first_name: str=None, last_name: str=None, email: str=None):  # noqa: E501
        """UserInfoInput - a model defined in Swagger

        :param user_id: The user_id of this UserInfoInput.  # noqa: E501
        :type user_id: str
        :param first_name: The first_name of this UserInfoInput.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this UserInfoInput.  # noqa: E501
        :type last_name: str
        :param email: The email of this UserInfoInput.  # noqa: E501
        :type email: str
        """
        self.swagger_types = {
            'user_id': str,
            'first_name': str,
            'last_name': str,
            'email': str
        }

        self.attribute_map = {
            'user_id': 'user_id',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email'
        }
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    @classmethod
    def from_dict(cls, dikt) -> 'UserInfoInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserInfoInput of this UserInfoInput.  # noqa: E501
        :rtype: UserInfoInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this UserInfoInput.


        :return: The user_id of this UserInfoInput.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this UserInfoInput.


        :param user_id: The user_id of this UserInfoInput.
        :type user_id: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def first_name(self) -> str:
        """Gets the first_name of this UserInfoInput.


        :return: The first_name of this UserInfoInput.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """Sets the first_name of this UserInfoInput.


        :param first_name: The first_name of this UserInfoInput.
        :type first_name: str
        """
        if first_name is None:
            raise ValueError("Invalid value for `first_name`, must not be `None`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """Gets the last_name of this UserInfoInput.


        :return: The last_name of this UserInfoInput.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """Sets the last_name of this UserInfoInput.


        :param last_name: The last_name of this UserInfoInput.
        :type last_name: str
        """
        if last_name is None:
            raise ValueError("Invalid value for `last_name`, must not be `None`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self) -> str:
        """Gets the email of this UserInfoInput.


        :return: The email of this UserInfoInput.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this UserInfoInput.


        :param email: The email of this UserInfoInput.
        :type email: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email
