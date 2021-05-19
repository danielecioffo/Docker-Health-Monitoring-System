# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.container import Container  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContainersController(BaseTestCase):
    """ContainersController integration test stubs"""

    def test_delete_monitored_container(self):
        """Test case for delete_monitored_container

        Unmonitor specified container
        """
        response = self.client.open(
            '/v2/containers/{hostname}/{containerName}'.format(hostname='hostname_example', containerName='containerName_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_containers(self):
        """Test case for get_containers

        Retrieve all containers
        """
        response = self.client.open(
            '/v2/containers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_container(self):
        """Test case for post_container

        Monitor specified container
        """
        response = self.client.open(
            '/v2/containers/{hostname}/{containerName}'.format(hostname='hostname_example', containerName='containerName_example'),
            method='POST',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
