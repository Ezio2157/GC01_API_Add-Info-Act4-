# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.success_response import SuccessResponse  # noqa: E501
from swagger_server.models.update_view_request import UpdateViewRequest  # noqa: E501
from swagger_server.models.view_request import ViewRequest  # noqa: E501
from swagger_server.models.view_response import ViewResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdditionalInfoController(BaseTestCase):
    """AdditionalInfoController integration test stubs"""

    def test_1_add_content_view(self):
        """Test case for add_content_view

        Add a view entry for content
        """
        body = ViewRequest(5)
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertEqual(response.status_code, 200,  # Reemplaza self.assert200
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_2_delete_content_view(self):
        """Test case for delete_content_view

        Delete view entry for content by user
        """
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='DELETE')
        self.assertEqual(response.status_code, 200,  # Reemplaza self.assert200
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_1_get_content_views(self):
        """Test case for get_content_views

        Get number of views for content
        """
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='GET')
        self.assertEqual(response.status_code, 200,  # Reemplaza self.assert200
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_1_update_content_view(self):
        """Test case for update_content_view

        Update view count for specific content and user
        """
        body = UpdateViewRequest(4)
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='PUT',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertEqual(response.status_code, 200,  # Reemplaza self.assert200
                         'Response body is : ' + response.data.decode('utf-8'))
