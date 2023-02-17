# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class FileFsBody1(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, file: str=None, workspace_id: str=None, file_id: str=None):  # noqa: E501
        """FileFsBody1 - a model defined in Swagger

        :param file: The file of this FileFsBody1.  # noqa: E501
        :type file: str
        :param workspace_id: The workspace_id of this FileFsBody1.  # noqa: E501
        :type workspace_id: str
        :param file_id: The file_id of this FileFsBody1.  # noqa: E501
        :type file_id: str
        """
        self.swagger_types = {
            'file': str,
            'workspace_id': str,
            'file_id': str
        }

        self.attribute_map = {
            'file': 'file',
            'workspace_id': 'workspace_id',
            'file_id': 'file_id'
        }
        self._file = file
        self._workspace_id = workspace_id
        self._file_id = file_id

    @classmethod
    def from_dict(cls, dikt) -> 'FileFsBody1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The file_fs_body_1 of this FileFsBody1.  # noqa: E501
        :rtype: FileFsBody1
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file(self) -> str:
        """Gets the file of this FileFsBody1.

        File to upload  # noqa: E501

        :return: The file of this FileFsBody1.
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file: str):
        """Sets the file of this FileFsBody1.

        File to upload  # noqa: E501

        :param file: The file of this FileFsBody1.
        :type file: str
        """

        self._file = file

    @property
    def workspace_id(self) -> str:
        """Gets the workspace_id of this FileFsBody1.

        Unique workspace object id  # noqa: E501

        :return: The workspace_id of this FileFsBody1.
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id: str):
        """Sets the workspace_id of this FileFsBody1.

        Unique workspace object id  # noqa: E501

        :param workspace_id: The workspace_id of this FileFsBody1.
        :type workspace_id: str
        """

        self._workspace_id = workspace_id

    @property
    def file_id(self) -> str:
        """Gets the file_id of this FileFsBody1.

        Unique file object id  # noqa: E501

        :return: The file_id of this FileFsBody1.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id: str):
        """Sets the file_id of this FileFsBody1.

        Unique file object id  # noqa: E501

        :param file_id: The file_id of this FileFsBody1.
        :type file_id: str
        """

        self._file_id = file_id
