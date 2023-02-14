# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from fluigi_cloud.models.workspace_info_input import WorkspaceInfoInput  # noqa: E501
from fluigi_cloud.models.workspace_input import WorkspaceInput  # noqa: E501
from fluigi_cloud.models.workspace_response import WorkspaceResponse  # noqa: E501
from fluigi_cloud.test import BaseTestCase


class TestWorkspaceController(BaseTestCase):
    """WorkspaceController integration test stubs"""

    def test_create_workspace(self):
        """Test case for create_workspace

        
        """
        body = WorkspaceInfoInput()
        response = self.client.open(
            '/api/v2/workspace',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_workspace(self):
        """Test case for delete_workspace

        
        """
        body = WorkspaceInput()
        response = self.client.open(
            '/api/v2/workspace',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_workspace_zip_fs(self):
        """Test case for get_workspace_zip_fs

        
        """
        body = WorkspaceInput()
        response = self.client.open(
            '/api/v2/workspace/zipfs',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_workspaces(self):
        """Test case for get_workspaces

        
        """
        body = WorkspaceInput()
        response = self.client.open(
            '/api/v2/workspace',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_workspace(self):
        """Test case for update_workspace

        
        """
        body = WorkspaceInfoInput()
        response = self.client.open(
            '/api/v2/workspace',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
