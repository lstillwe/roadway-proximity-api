# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.roadway_data import RoadwayData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_distance(self):
        """Test case for get_distance

        retrieves distance
        """
        query_string = [('latitude', 1.2),
                        ('longitude', 1.2),
                        ('limit_distance', 500.0)]
        response = self.client.open(
            '/proximity_api/roadway_proximity_aos2/1.0.0/distance',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
