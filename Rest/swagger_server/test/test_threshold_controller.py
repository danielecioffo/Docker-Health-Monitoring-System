# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestThresholdController(BaseTestCase):
    """ThresholdController integration test stubs"""

    def test_put_threshold(self):
        """Test case for put_threshold

        Update packet loss threshold
        """
        thresholdValue = 1.2
        response = self.client.open(
            '/v2/threshold',
            method='PUT',
            data=json.dumps(thresholdValue),
            content_type='application/xml')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
