# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from fluigi_cloud.models.base_model_ import Model
from fluigi_cloud import util


class FileCopyBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, file_id: str=None, workspace_id: str=None):  # noqa: E501
        """FileCopyBody - a model defined in Swagger

        :param file_id: The file_id of this FileCopyBody.  # noqa: E501
        :type file_id: str
        :param workspace_id: The workspace_id of this FileCopyBody.  # noqa: E501
        :type workspace_id: str
        """
        self.swagger_types = {
            'file_id': str,
            'workspace_id': str
        }

        self.attribute_map = {
            'file_id': 'file_id',
            'workspace_id': 'workspace_id'
        }
        self._file_id = file_id
        self._workspace_id = workspace_id

    @classmethod
    def from_dict(cls, dikt) -> 'FileCopyBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The file_copy_body of this FileCopyBody.  # noqa: E501
        :rtype: FileCopyBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file_id(self) -> str:
        """Gets the file_id of this FileCopyBody.

        Unique file object id  # noqa: E501

        :return: The file_id of this FileCopyBody.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id: str):
        """Sets the file_id of this FileCopyBody.

        Unique file object id  # noqa: E501

        :param file_id: The file_id of this FileCopyBody.
        :type file_id: str
        """

        self._file_id = file_id

    @property
    def workspace_id(self) -> str:
        """Gets the workspace_id of this FileCopyBody.

        Unique workspace object id  # noqa: E501

        :return: The workspace_id of this FileCopyBody.
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id: str):
        """Sets the workspace_id of this FileCopyBody.

        Unique workspace object id  # noqa: E501

        :param workspace_id: The workspace_id of this FileCopyBody.
        :type workspace_id: str
        """

        self._workspace_id = workspace_id