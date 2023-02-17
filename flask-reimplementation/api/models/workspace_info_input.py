# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class WorkspaceInfoInput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, workspace_id: str=None, workspace_name: str=None):  # noqa: E501
        """WorkspaceInfoInput - a model defined in Swagger

        :param workspace_id: The workspace_id of this WorkspaceInfoInput.  # noqa: E501
        :type workspace_id: str
        :param workspace_name: The workspace_name of this WorkspaceInfoInput.  # noqa: E501
        :type workspace_name: str
        """
        self.swagger_types = {
            'workspace_id': str,
            'workspace_name': str
        }

        self.attribute_map = {
            'workspace_id': 'workspace_id',
            'workspace_name': 'workspace_name'
        }
        self._workspace_id = workspace_id
        self._workspace_name = workspace_name

    @classmethod
    def from_dict(cls, dikt) -> 'WorkspaceInfoInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The WorkspaceInfoInput of this WorkspaceInfoInput.  # noqa: E501
        :rtype: WorkspaceInfoInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def workspace_id(self) -> str:
        """Gets the workspace_id of this WorkspaceInfoInput.

        Unique workspace object id  # noqa: E501

        :return: The workspace_id of this WorkspaceInfoInput.
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id: str):
        """Sets the workspace_id of this WorkspaceInfoInput.

        Unique workspace object id  # noqa: E501

        :param workspace_id: The workspace_id of this WorkspaceInfoInput.
        :type workspace_id: str
        """
        if workspace_id is None:
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

    @property
    def workspace_name(self) -> str:
        """Gets the workspace_name of this WorkspaceInfoInput.

        Workspace name  # noqa: E501

        :return: The workspace_name of this WorkspaceInfoInput.
        :rtype: str
        """
        return self._workspace_name

    @workspace_name.setter
    def workspace_name(self, workspace_name: str):
        """Sets the workspace_name of this WorkspaceInfoInput.

        Workspace name  # noqa: E501

        :param workspace_name: The workspace_name of this WorkspaceInfoInput.
        :type workspace_name: str
        """
        if workspace_name is None:
            raise ValueError("Invalid value for `workspace_name`, must not be `None`")  # noqa: E501

        self._workspace_name = workspace_name
