# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class JobInput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, job_id: str=None):  # noqa: E501
        """JobInput - a model defined in Swagger

        :param job_id: The job_id of this JobInput.  # noqa: E501
        :type job_id: str
        """
        self.swagger_types = {
            'job_id': str
        }

        self.attribute_map = {
            'job_id': 'job_id'
        }
        self._job_id = job_id

    @classmethod
    def from_dict(cls, dikt) -> 'JobInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The JobInput of this JobInput.  # noqa: E501
        :rtype: JobInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def job_id(self) -> str:
        """Gets the job_id of this JobInput.


        :return: The job_id of this JobInput.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id: str):
        """Sets the job_id of this JobInput.


        :param job_id: The job_id of this JobInput.
        :type job_id: str
        """
        if job_id is None:
            raise ValueError("Invalid value for `job_id`, must not be `None`")  # noqa: E501

        self._job_id = job_id
