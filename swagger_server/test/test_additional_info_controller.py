# coding: utf-8

from __future__ import absolute_import

from flask import json
from requests.cookies import MockResponse
from six import BytesIO
import pytest
from unittest.mock import patch
from requests.models import Response

from swagger_server.models.continuewatching_content_id_body import ContinuewatchingContentIdBody  # noqa: E501
from swagger_server.models.continuewatching_content_id_body1 import ContinuewatchingContentIdBody1  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.success_response import SuccessResponse  # noqa: E501
from swagger_server.models.update_view_request import UpdateViewRequest  # noqa: E501
from swagger_server.models.view_request import ViewRequest  # noqa: E501
from swagger_server.models.view_response import ViewResponse  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.test.MockResponse import MockResponse

BASE_URL_USER_SERVER = "http://localhost:8082/v1"
BASE_URL_CONTENT_API = "http://localhost:8081/v1"

@pytest.fixture
def mock_get_content_languages():
    with patch('swagger_server.controllers.additional_info_controller.requests.get') as mock_get:
        def side_effect(url, *args, **kwargs):
            # Verifica si la URL corresponde a obtener detalles de un contenido específico
            if url.startswith(f"{BASE_URL_CONTENT_API}/contents/"):
                # Extrae el content_id de la URL
                parts = url.rstrip('/').split('/')
                try:
                    content_id = parts[-1]
                    # Verifica que content_id sea un número
                    int(content_id)
                except (IndexError, ValueError):
                    # Si no se puede extraer o no es un número, retorna 404
                    mock_resp = Response()
                    mock_resp.status_code = 404
                    mock_resp._content = b'{"error": "Not found"}'
                    return mock_resp

                # Define respuestas mockeadas para diferentes content_id
                mock_languages = {
                    "1": "english",
                    "2": "spanish",
                    "3": "french",
                    "4": "german"
                }

                # Obtiene el idioma para el content_id solicitado
                language = mock_languages.get(content_id)

                if language:
                    mock_content = {
                        "id": int(content_id),
                        "title": f"Title{content_id}",
                        "language": language  # Nota: "language" en singular y en minúsculas
                    }
                    mock_resp = Response()
                    mock_resp.status_code = 200
                    mock_resp._content = json.dumps(mock_content).encode('utf-8')
                    return mock_resp
                else:
                    # Si el content_id no está definido en el mock, retorna 404
                    mock_resp = Response()
                    mock_resp.status_code = 404
                    mock_resp._content = b'{"error": "Not found"}'
                    return mock_resp
            else:
                # Respuesta por defecto para URLs no esperadas
                mock_resp = Response()
                mock_resp.status_code = 404
                mock_resp._content = b'{"error": "Not found"}'
                return mock_resp

        mock_get.side_effect = side_effect
        yield mock_get

@pytest.fixture
def mock_get_recommendations():
    with patch('swagger_server.controllers.additional_info_controller.requests.get') as mock_get:
        def side_effect(url, *args, **kwargs):
            # Mock para obtener la lista de contenidos favoritos
            if url == f"{BASE_URL_USER_SERVER}/users/56/profiles/56/lists/favorites":
                mock_resp = Response()
                mock_resp.status_code = 200
                mock_resp._content = b'[1, 2, 3]'  # IDs de contenidos favoritos
                return mock_resp

            # Mock para obtener información de un contenido específico
            elif url.startswith(f"{BASE_URL_CONTENT_API}/contents/") and not url.endswith("/contents"):
                content_id = url.split('/')[-1]
                mock_resp = Response()
                mock_resp.status_code = 200
                if content_id.isdigit():
                    content_id = int(content_id)
                    # Define géneros según el ID para variar los datos
                    genre = "comedy" if content_id % 2 else "drama"
                    mock_content = {
                        "id": content_id,
                        "title": f"Title{content_id}",
                        "genre": genre
                    }
                else:
                    mock_content = {"id": 0, "title": "Unknown", "genre": "unknown"}
                mock_resp._content = json.dumps(mock_content).encode('utf-8')
                return mock_resp

            # Mock para obtener todos los contenidos
            elif url == f"{BASE_URL_CONTENT_API}/contents":
                mock_resp = Response()
                mock_resp.status_code = 200
                all_contents = [
                    {"id": 1, "title": "Title1", "genre": "comedy"},
                    {"id": 2, "title": "Title2", "genre": "drama"},
                    {"id": 3, "title": "Title3", "genre": "comedy"},
                    {"id": 4, "title": "Title4", "genre": "action"},
                ]
                mock_resp._content = json.dumps(all_contents).encode('utf-8')
                return mock_resp

            # Respuesta por defecto para URLs no esperadas
            else:
                mock_resp = Response()
                mock_resp.status_code = 404
                mock_resp._content = b'{"error": "Not found"}'
                return mock_resp

        mock_get.side_effect = side_effect
        yield mock_get

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
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_2_delete_content_view(self):
        """Test case for delete_content_view

        Delete view entry for content by user
        """
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='DELETE')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_1_get_content_views(self):
        """Test case for get_content_views

        Get number of views for content
        """
        response = self.client.open(
            '/v1/contents/{content_id}/views'.format(content_id=56),
            method='GET')
        self.assertEqual(response.status_code, 200,
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
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    @pytest.mark.usefixtures("mock_get_content_languages")
    def test_1_get_content_languages(self):
        """Test case for get_content_languages

        Get available languages for content
        """
        # Usa un content_id que esté definido en el mock, por ejemplo, 1
        response = self.client.open(
            '/v1/contents/{content_id}/languages'.format(content_id=1),
            method='GET')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

        # Verificar el contenido de la respuesta
        response_data = json.loads(response.data.decode('utf-8'))
        expected_languages = {"languages": "english"}  # Dado que cada película tiene un solo idioma
        self.assertEqual(response_data, expected_languages,
                         'Los lenguajes no coinciden con lo esperado')

    @pytest.mark.usefixtures("mock_get_recommendations")
    def test_1_get_recommendations_for_user(self):
        """Test case for get_recommendations_for_user

        Get recommendations for a profile
        """
        response = self.client.open(
            '/v1/users/{user_id}/profiles/{profile_id}/recommendations'.format(user_id=56, profile_id=56),
            method='GET')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

        # Verificar el contenido de la respuesta
        response_data = json.loads(response.data.decode('utf-8'))
        expected_recommendations = [
            {"contentId": 1, "title": "Title1"},
            {"contentId": 2, "title": "Title2"},
            {"contentId": 3, "title": "Title3"}
        ]
        self.assertEqual(response_data['recommendations'], expected_recommendations,
                         'Las recomendaciones no coinciden con lo esperado')

    def test_1_add_continue_watching(self):
        """Test case for add_continue_watching

        Add continue watching entry
        """
        body = ContinuewatchingContentIdBody1(30)
        response = self.client.open(
            '/v1/users/{user_id}/profiles/{profile_id}/continue-watching/{content_id}'.format(user_id=56, profile_id=56,
                                                                                              content_id=56),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_2_delete_continue_watching(self):
        """Test case for delete_continue_watching

        Delete continue watching entry
        """
        response = self.client.open(
            '/v1/users/{user_id}/profiles/{profile_id}/continue-watching/{content_id}'.format(user_id=56, profile_id=56,
                                                                                              content_id=56),
            method='DELETE')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_1_get_continue_watching(self):
        """Test case for get_continue_watching

        Get last watched minute for content
        """
        response = self.client.open(
            '/v1/users/{user_id}/profiles/{profile_id}/continue-watching/{content_id}'.format(user_id=56, profile_id=56,
                                                                                              content_id=56),
            method='GET')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))

    def test_1_update_continue_watching(self):
        """Test case for update_continue_watching

        Update continue watching entry
        """
        body = ContinuewatchingContentIdBody(60)
        response = self.client.open(
            '/v1/users/{user_id}/profiles/{profile_id}/continue-watching/{content_id}'.format(user_id=56, profile_id=56,
                                                                                              content_id=56),
            method='PUT',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertEqual(response.status_code, 200,
                         'Response body is : ' + response.data.decode('utf-8'))