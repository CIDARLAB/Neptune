# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.login_input import LoginInput  # noqa: E501
from swagger_server.models.register_input import RegisterInput  # noqa: E501
from swagger_server.models.user_response import UserResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAuthenticationController(BaseTestCase):
    """AuthenticationController integration test stubs"""

    def test_login_user(self):
        """Test case for login_user

        Login a user
        """
        body = LoginInput()
        response = self.client.open(
            '/api/v2/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_user(self):
        """Test case for register_user

        Register a new user
        """
        body = RegisterInput()
        response = self.client.open(
            '/api/v2/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
