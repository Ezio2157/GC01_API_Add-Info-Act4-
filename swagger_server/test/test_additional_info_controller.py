# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.users_user_id_body import UsersUserIdBody  # noqa: E501
from swagger_server.models.users_user_id_body1 import UsersUserIdBody1  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdditionalInfoController(BaseTestCase):
    """AdditionalInfoController integration test stubs"""

    def test_add_numeric_review_for_content(self):
        """Test case for add_numeric_review_for_content

        Add a numeric review for content
        """
        body = UsersUserIdBody1()
        response = self.client.open(
            '/v1/contents/{contentId}/reviews/users/{userId}'.format(content_id=56, user_id=56),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_specific_review_for_content_by_user(self):
        """Test case for delete_specific_review_for_content_by_user

        Delete a specific review for content by user
        """
        response = self.client.open(
            '/v1/contents/{contentId}/reviews/users/{userId}'.format(content_id=56, user_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_content_languages(self):
        """Test case for get_content_languages

        Get available languages for content
        """
        response = self.client.open(
            '/v1/contents/{contentId}/languages'.format(content_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_content_views(self):
        """Test case for get_content_views

        Get number of views for content
        """
        response = self.client.open(
            '/v1/contents/{contentId}/views'.format(content_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_numeric_review_for_content_by_user(self):
        """Test case for get_numeric_review_for_content_by_user

        Get a specific review for content by user
        """
        response = self.client.open(
            '/v1/contents/{contentId}/reviews/users/{userId}'.format(content_id=56, user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_numeric_reviews_by_user(self):
        """Test case for get_numeric_reviews_by_user

        Get reviews by user
        """
        response = self.client.open(
            '/v1/users/{userId}/reviews'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_numeric_reviews_for_content(self):
        """Test case for get_numeric_reviews_for_content

        Get numeric reviews for specific content
        """
        response = self.client.open(
            '/v1/contents/{contentId}/reviews'.format(content_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_recommendations_for_user(self):
        """Test case for get_recommendations_for_user

        Get recommendations for a profile
        """
        response = self.client.open(
            '/v1/users/{userId}/profiles/{profileId}/recommendations'.format(user_id=56, profile_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_specific_review_for_content_by_user(self):
        """Test case for update_specific_review_for_content_by_user

        Update a specific review for content by user
        """
        body = UsersUserIdBody()
        response = self.client.open(
            '/v1/contents/{contentId}/reviews/users/{userId}'.format(content_id=56, user_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
