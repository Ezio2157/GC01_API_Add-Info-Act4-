import connexion
import requests

from swagger_server.services.view_service import *
from swagger_server.services.continue_watching_service import *
from swagger_server.services.review_service import *
from swagger_server.models.continuewatching_content_id_body import ContinuewatchingContentIdBody  # noqa: E501
from swagger_server.models.continuewatching_content_id_body1 import ContinuewatchingContentIdBody1  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.success_response import SuccessResponse  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.review_request import ReviewRequest  # noqa: E501
from swagger_server.models.review_response import ReviewResponse  # noqa: E501
from swagger_server.models.reviews_response import ReviewsResponse  # noqa: E501
from swagger_server.models.success_response import SuccessResponse  # noqa: E501
from swagger_server.models.update_review_request import UpdateReviewRequest  # noqa: E501
from swagger_server.models.success_response import SuccessResponse  # noqa: E501
from swagger_server.models.update_view_request import UpdateViewRequest  # noqa: E501
from swagger_server.models.view_request import ViewRequest  # noqa: E501
from swagger_server.models.view_response import ViewResponse  # noqa: E501
from swagger_server import util

BASE_URL_USER_SERVER = "http://localhost:8082/v1"
BASE_URL_CONTENT_API = "http://localhost:8081/v1"

DELETE_MESSAGE = 'No record found to delete'
UPDATE_MESSAGE = 'No record found to update'

def add_numeric_review_for_content(content_id, user_id, profile_id, body):  # noqa: E501
    """Add a numeric review for content

    Submit a numeric review for a specific content by a user # noqa: E501

    :param body: The review data
    :type body: dict | bytes
    :param content_id: The ID of the content to review
    :type content_id: int
    :param user_id: The ID of the user submitting the review
    :type user_id: int
    :param profile_id: The ID of the profile submitting the review
    :type profile_id: int

    :rtype: SuccessResponse
    """
    rating = body.get('rating')

    # Validar el rango de la calificación
    if not (1 <= rating <= 5):
        return {'error': 'Rating must be between 1 and 5'}, 400

    # Llama a la función de base de datos para agregar la reseña
    result = insert_review(content_id, user_id, profile_id, rating)

    if result['status'] == 'success':
        response = SuccessResponse(message='Review added successfully')
        return response, 200
    else:
        return {'error': result['error']}, 400


def delete_numeric_review_for_content(content_id, user_id, profile_id):  # noqa: E501
    """Delete a specific review for content by user

    Delete a specific numeric review for a given content and user # noqa: E501

    :param content_id: The ID of the content to delete the review for
    :type content_id: int
    :param user_id: The ID of the user whose review is to be deleted
    :type user_id: int
    :param profile_id: The ID of the profile whose review is to be deleted
    :type profile_id: int

    :rtype: SuccessResponse
    """
    result = delete_review(content_id, user_id, profile_id)

    if result['status'] == 'success' and result['rowcount'] > 0:
        response = SuccessResponse(message='Review deleted successfully')
        return response, 200
    elif result['status'] == 'success':
        response = SuccessResponse(message=DELETE_MESSAGE)
        return response, 404
    else:
        return {'error': result['error']}, 400


def get_numeric_review_for_content_by_user_and_profile(content_id, user_id, profile_id):  # noqa: E501
    """Get a specific review for content by user

    Retrieve a specific numeric review made by a user for a given content # noqa: E501

    :param content_id: The ID of the content to retrieve the review for
    :type content_id: int
    :param user_id: The ID of the user whose review to retrieve
    :type user_id: int
    :param profile_id: The ID of the profile
    :type profile_id: int

    :rtype: ReviewResponse
    """
    result = fetch_review(content_id, user_id, profile_id)

    if result['status'] == 'success' and result['data']:
        review_data = result['data'][0]
        response = ReviewResponse(
            content_id=review_data['content_id'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            profile_id=review_data['profile_id']
        )
        return response, 200
    elif result['status'] == 'success':
        return {'message': 'No record found'}, 404
    else:
        return {'error': result['error']}, 400


def get_numeric_reviews_by_user(user_id):  # noqa: E501
    """Get reviews by user

    Retrieve all numeric reviews made by a specific user # noqa: E501

    :param user_id: The ID of the user whose reviews to retrieve
    :type user_id: int

    :rtype: ReviewsResponse
    """
    result = fetch_reviews_by_user(user_id)

    if result['status'] == 'success' and result['data']:
        formatted_reviews = [
            {
                "profile_id": review["profile_id"],
                "content_id": review["content_id"],
                "rating": review["rating"],
                "user_id": review["user_id"]
            }
            for review in result['data']
        ]
        response = ReviewsResponse(reviews=formatted_reviews)
        return response, 200
    elif result['status'] == 'success':
        return {'message': 'No reviews found for this user'}, 404
    else:
        return {'error': result['error']}, 400


def get_numeric_reviews_for_content(content_id):  # noqa: E501
    """Get numeric reviews for specific content

    Retrieve all numeric reviews (user ID and rating) made for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve reviews for
    :type content_id: int

    :rtype: ReviewsResponse
    """
    result = fetch_reviews_for_content(content_id)

    if result['status'] == 'success' and result['data']:
        formatted_reviews = [
            {
                "contentId": review["content_id"],
                "rating": review["rating"],
                "userId": review["user_id"],
                "profileId": review["profile_id"]
            }
            for review in result['data']
        ]
        response = ReviewsResponse(reviews=formatted_reviews)
        return response, 200
    elif result['status'] == 'success':
        response = ReviewsResponse(reviews=[])
        return response, 404  # Devuelve una lista vacía con el código 404 para representar que no hay reseñas
    else:
        return {'error': result['error']}, 400


def update_numeric_review_for_content_by_user_and_profile(content_id, user_id, profile_id, body):  # noqa: E501
    """Update a specific review for content by user

    Update an existing numeric review for a given content and user # noqa: E501

    :param body: The updated review data
    :type body: dict | bytes
    :param content_id: The ID of the content to update the review for
    :type content_id: int
    :param user_id: The ID of the user whose review is being updated
    :type user_id: int
    :param profile_id: The ID of the profile whose review is being updated
    :type profile_id: int

    :rtype: SuccessResponse
    """
    new_rating = body.get('rating')

    # Validar el rango de la calificación
    if not (1 <= new_rating <= 5):
        return {'error': 'Rating must be between 1 and 5'}, 400

    result = update_review(content_id, user_id, profile_id, new_rating)
    if result['status'] == 'success' and result['rowcount'] > 0:
        response = SuccessResponse(message='Review updated successfully')
        return response, 200
    elif result['status'] == 'success':
        response = SuccessResponse(message=UPDATE_MESSAGE)
        return response, 404
    else:
        return {'error': result['error']}, 400


def get_content_languages(content_id):  # noqa: E501
    """Get available languages for content

    Retrieve a list of available languages for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve languages for
    :type content_id: int

    :rtype: InlineResponse2001
    """
    # Llama al endpoint que obtiene todos los detalles del contenido
    response = requests.get(f"{BASE_URL_CONTENT_API}/contents/{content_id}")

    if response.status_code == 200:
        try:
            # Extrae la respuesta JSON completa
            content_data = response.json()
            # Extrae solo la parte de "languages" del contenido
            language = content_data.get("language", [])
            # Devuelve los idiomas en la estructura esperada por InlineResponse2005
            response_model = InlineResponse2001(languages=language)
            return response_model, response.status_code
        except ValueError:
            # Maneja el caso donde la respuesta no es JSON válido
            return {"error": "Respuesta no es JSON válida"}, 500
    else:
        return {"error": f"Error en el microservicio de contenido: {response.status_code}"}, response.status_code


def get_recommendations_for_user(user_id, profile_id):  # noqa: E501
    """Get recommendations for a profile

    Retrieve content recommendations based on a user&#x27;s viewing history # noqa: E501

    :param user_id: The ID of the user to retrieve recommendations for
    :type user_id: int
    :param profile_id: The ID of the profile to retrieve recommendations for
    :type profile_id: int

    :rtype: InlineResponse2002
    """
    # Paso 1: Obtener los IDs de los contenidos favoritos del perfil
    response = requests.get(f"{BASE_URL_USER_SERVER}/users/{user_id}/profiles/{profile_id}/lists/favorites")
    if response.status_code != 200:
        return {"error": "No se pudieron obtener los favoritos"}, response.status_code

    # Extraer los IDs de contenidos favoritos
    favorite_content_ids = response.json()

    # Paso 2: Obtener los géneros de los contenidos favoritos
    favorite_genres = set()
    for content_id in favorite_content_ids:
        content_response = requests.get(f"{BASE_URL_CONTENT_API}/contents/{content_id}")
        if content_response.status_code == 200:
            content_data = content_response.json()
            genre = content_data.get("genre")
            if genre:
                favorite_genres.add(genre)

    # Paso 3: Buscar todos los contenidos que coincidan con los géneros favoritos
    recommendations = []
    all_contents_response = requests.get(f"{BASE_URL_CONTENT_API}/contents")
    if all_contents_response.status_code != 200:
        return {"error": "No se pudieron obtener los contenidos"}, all_contents_response.status_code

    all_contents = all_contents_response.json()
    for content in all_contents:
        if content.get("genre") in favorite_genres:
            # Agrega solo contentId y title a la lista de recomendaciones
            recommendations.append({
                "contentId": content["id"],
                "title": content["title"]
            })

    # Paso 4: Devolver las recomendaciones en el formato esperado
    response_model = InlineResponse2002(recommendations=recommendations)
    return response_model, 200


def get_content_views(content_id):  # noqa: E501
    """Get number of views for content

    Retrieve the number of views for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve views for
    :type content_id: int

    :rtype: ViewResponse
    """
    result = fetch_view_count(content_id)

    if result['status'] == 'success':
        views = result['data'][0]['view_count'] if result['data'] else 0
        response_model = ViewResponse(views=views)
        return response_model, 200
    else:
        return {'error': result['error']}, 400


def add_content_view(content_id, body):
    """Add a view entry for content

    Add a new view entry for a specific content. # noqa: E501

    :param body: Data for the new view entry
    :type body: dict | bytes
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    view_count = body.get('view_count')

    result = add_view(content_id, view_count)

    if result['status'] == 'success':
        response_model = SuccessResponse(message='View added successfully')
        return response_model, 200
    else:
        return {'error': result['error']}, 400


def update_content_view(content_id, body):
    """Update view count for specific content and user

    Update the view count for a specific content by a user. # noqa: E501

    :param body: Updated view count
    :type body: dict | bytes
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    new_view_count = body.get('new_view_count')
    result = update_view(content_id, new_view_count)

    if result['status'] == 'success' and result['rowcount'] > 0:
        response_model = SuccessResponse(message='View count updated successfully')
        return response_model, 200
    elif result['status'] == 'success':
        response_model = SuccessResponse(message=UPDATE_MESSAGE)
        return response_model, 404
    else:
        return {'error': result['error']}, 400


def delete_content_view(content_id):
    """Delete view entry for content by user

    Delete a view entry for a specific content and user. # noqa: E501

    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    result = delete_view(int(content_id))

    if result['status'] == 'success' and result['rowcount'] > 0:
        response_model = SuccessResponse(message='View deleted successfully')
        return response_model, 200
    elif result['status'] == 'success':
        response_model = SuccessResponse(message=DELETE_MESSAGE)
        return response_model, 404
    else:
        return {'error': result['error']}, 400


def get_continue_watching(user_id, profile_id, content_id):
    """Get last watched minute for content

    Retrieve the last watched minute for a specific content by a user and profile. # noqa: E501

    :param user_id: The ID of the user
    :type user_id: int
    :param profile_id: The ID of the profile
    :type profile_id: int
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: InlineResponse200
    """
    result = fetch_continue_watching(user_id, profile_id, content_id)

    if result['status'] == 'success' and result['data']:
        response_model = InlineResponse200(last_watched_minute=result['data'][0]['last_watched_minute'])
        return response_model, 200
    elif result['status'] == 'success':
        return {'message': 'No record found'}, 404
    else:
        return {'error': result['error']}, 400


def add_continue_watching(user_id, profile_id, content_id, body):
    """Add continue watching entry

    Add a new entry for a user&#x27;s last watched minute for a specific content. # noqa: E501

    :param body: Data for the continue watching entry
    :type body: dict | bytes
    :param user_id: The ID of the user
    :type user_id: int
    :param profile_id: The ID of the profile
    :type profile_id: int
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    last_watched_minute = body.get('last_watched_minute')
    result = insert_continue_watching(user_id, profile_id, content_id, last_watched_minute)

    if result['status'] == 'success':
        response_model = SuccessResponse(message='Continue watching entry created successfully')
        return response_model, 200
    else:
        return {'error': result['error']}, 400


def update_continue_watching(user_id, profile_id, content_id, body):
    """Update continue watching entry

    Update the last watched minute for a user&#x27;s content. # noqa: E501

    :param body: Updated continue watching data
    :type body: dict | bytes
    :param user_id: The ID of the user
    :type user_id: int
    :param profile_id: The ID of the profile
    :type profile_id: int
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    new_last_watched_minute = body.get('new_last_watched_minute')
    result = update_continue_entry(user_id, profile_id, content_id, new_last_watched_minute)
    if result['status'] == 'success' and result['rowcount'] > 0:
        response_model = SuccessResponse(message='Continue watching entry updated successfully')
        return response_model, 200
    elif result['status'] == 'success':
        response_model = SuccessResponse(message=UPDATE_MESSAGE)
        return response_model, 404
    else:
        return {'error': result['error']}, 400

def delete_continue_watching(user_id, profile_id, content_id):
    """Delete continue watching entry

    Delete a continue watching entry for a specific content by a user and profile. # noqa: E501

    :param user_id: The ID of the user
    :type user_id: int
    :param profile_id: The ID of the profile
    :type profile_id: int
    :param content_id: The ID of the content
    :type content_id: int

    :rtype: SuccessResponse
    """
    result = delete_continue_entry(user_id, profile_id, content_id)
    if result['status'] == 'success' and result['rowcount'] > 0:
        response_model = SuccessResponse(message='Continue watching entry deleted successfully')
        return response_model, 200
    elif result['status'] == 'success':
        response_model = SuccessResponse(message=DELETE_MESSAGE)
        return response_model, 404
    else:
        return {'error': result['error']}, 400
