# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.models.user_info_input import UserInfoInput  # noqa: E501
from api.models.user_response import UserResponse  # noqa: E501
from api.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_get_user(self):
        """Test case for get_user

        Get user information
        """
        response = self.client.open(
            '/api/v2/user',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Update user information
        """
        body = UserInfoInput()
        response = self.client.open(
            '/api/v2/user',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
