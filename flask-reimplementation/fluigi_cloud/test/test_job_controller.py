# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from fluigi_cloud.models.job_input import JobInput  # noqa: E501
from fluigi_cloud.models.job_response import JobResponse  # noqa: E501
from fluigi_cloud.test import BaseTestCase


class TestJobController(BaseTestCase):
    """JobController integration test stubs"""

    def test_delete_job(self):
        """Test case for delete_job

        
        """
        body = JobInput()
        response = self.client.open(
            '/api/v2/job',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_job_zip_fs(self):
        """Test case for get_job_zip_fs

        
        """
        body = JobInput()
        response = self.client.open(
            '/api/v2/job/zipfs',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_jobs(self):
        """Test case for get_jobs

        
        """
        body = JobInput()
        response = self.client.open(
            '/api/v2/job',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
