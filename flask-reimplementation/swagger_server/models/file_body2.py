# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class FileBody2(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, file_name: str=None, workspace_id: str=None):  # noqa: E501
        """FileBody2 - a model defined in Swagger

        :param file_name: The file_name of this FileBody2.  # noqa: E501
        :type file_name: str
        :param workspace_id: The workspace_id of this FileBody2.  # noqa: E501
        :type workspace_id: str
        """
        self.swagger_types = {
            'file_name': str,
            'workspace_id': str
        }

        self.attribute_map = {
            'file_name': 'file_name',
            'workspace_id': 'workspace_id'
        }
        self._file_name = file_name
        self._workspace_id = workspace_id

    @classmethod
    def from_dict(cls, dikt) -> 'FileBody2':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The file_body_2 of this FileBody2.  # noqa: E501
        :rtype: FileBody2
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file_name(self) -> str:
        """Gets the file_name of this FileBody2.

        Name of the file  # noqa: E501

        :return: The file_name of this FileBody2.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        """Sets the file_name of this FileBody2.

        Name of the file  # noqa: E501

        :param file_name: The file_name of this FileBody2.
        :type file_name: str
        """

        self._file_name = file_name

    @property
    def workspace_id(self) -> str:
        """Gets the workspace_id of this FileBody2.

        Unique workspace object id  # noqa: E501

        :return: The workspace_id of this FileBody2.
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id: str):
        """Sets the workspace_id of this FileBody2.

        Unique workspace object id  # noqa: E501

        :param workspace_id: The workspace_id of this FileBody2.
        :type workspace_id: str
        """

        self._workspace_id = workspace_id
