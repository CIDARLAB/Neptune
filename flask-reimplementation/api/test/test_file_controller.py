# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.models.file_body import FileBody  # noqa: E501
from api.models.file_body1 import FileBody1  # noqa: E501
from api.models.file_body2 import FileBody2  # noqa: E501
from api.models.file_body3 import FileBody3  # noqa: E501
from api.models.file_copy_body import FileCopyBody  # noqa: E501
from api.models.file_fs_body import FileFsBody  # noqa: E501
from api.models.file_response import FileResponse  # noqa: E501
from api.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    def test_copy_file(self):
        """Test case for copy_file

        
        """
        body = FileCopyBody()
        response = self.client.open(
            '/api/v2/file/copy',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_file(self):
        """Test case for create_file

        Create a new file
        """
        body = FileBody2()
        response = self.client.open(
            '/api/v2/file',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_file(self):
        """Test case for delete_file

        Delete a file
        """
        body = FileBody3()
        response = self.client.open(
            '/api/v2/file',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file(self):
        """Test case for get_file

        Get file information
        """
        body = FileBody()
        response = self.client.open(
            '/api/v2/file',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file_fs(self):
        """Test case for get_file_fs

        
        """
        body = FileFsBody()
        response = self.client.open(
            '/api/v2/file/fs',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_file_fs(self):
        """Test case for post_file_fs

        
        """
        data = dict(file='file_example',
                    workspace_id='workspace_id_example')
        response = self.client.open(
            '/api/v2/file/fs',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_file_fs(self):
        """Test case for put_file_fs

        
        """
        data = dict(file='file_example',
                    workspace_id='workspace_id_example',
                    file_id='file_id_example')
        response = self.client.open(
            '/api/v2/file/fs',
            method='PUT',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_file(self):
        """Test case for update_file

        Update a file's properties
        """
        body = FileBody1()
        response = self.client.open(
            '/api/v2/file',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
