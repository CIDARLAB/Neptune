# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.compiler_inputs import CompilerInputs  # noqa: E501
from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCompileController(BaseTestCase):
    """CompileController integration test stubs"""

    def test_compile_lfr(self):
        """Test case for compile_lfr

        
        """
        body = CompilerInputs()
        response = self.client.open(
            '/api/v2/compile/lfr',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_compile_mint(self):
        """Test case for compile_mint

        
        """
        body = CompilerInputs()
        response = self.client.open(
            '/api/v2/compile/mint',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_run_test_job(self):
        """Test case for run_test_job

        
        """
        body = CompilerInputs()
        response = self.client.open(
            '/api/v2/compile/test',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
