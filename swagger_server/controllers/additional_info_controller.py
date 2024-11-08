import connexion
import requests

from swagger_server.services.view_service import *
from swagger_server.services.continue_watching_service import *
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
from swagger_server import util

BASE_URL_USER_SERVER = "http://localhost:8082/v1"
BASE_URL_CONTENT_API = "http://localhost:8081/v1"

def add_numeric_review_for_content(body, content_id, user_id):  # noqa: E501
    """Add a numeric review for content

    Submit a numeric review for a specific content by a user # noqa: E501

    :param body: The review data
    :type body: dict | bytes
    :param content_id: The ID of the content to review
    :type content_id: int
    :param user_id: The ID of the user submitting the review
    :type user_id: int

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        body = UsersUserIdBody1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_specific_review_for_content_by_user(content_id, user_id):  # noqa: E501
    """Delete a specific review for content by user

    Delete a specific numeric review for a given content and user # noqa: E501

    :param content_id: The ID of the content to delete the review for
    :type content_id: int
    :param user_id: The ID of the user whose review is to be deleted
    :type user_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_content_languages(content_id):  # noqa: E501
    """Get available languages for content

    Retrieve a list of available languages for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve languages for
    :type content_id: int

    :rtype: InlineResponse2005
    """
    # Llama al endpoint que obtiene todos los detalles del contenido
    response = requests.get(f"{BASE_URL_CONTENT_API}/contents/{content_id}")

    # Verifica si la respuesta es exitosa (código 200)
    if response.status_code == 200:
        try:
            # Extrae la respuesta JSON completa
            content_data = response.json()
            # Extrae solo la parte de "languages" del contenido
            languages = content_data.get("languages", [])
            # Devuelve los idiomas en la estructura esperada por InlineResponse2005
            return InlineResponse2005.from_dict({"languages": languages}), response.status_code
        except ValueError:
            # Maneja el caso donde la respuesta no es JSON válido
            return {"error": "Respuesta no es JSON válida"}, 500
    else:
        # Si el estado no es 200, devuelve un mensaje de error con el estado de respuesta
        return {"error": f"Error en el microservicio de contenido: {response.status_code}"}, response.status_code


def get_numeric_review_for_content_by_user(content_id, user_id):  # noqa: E501
    """Get a specific review for content by user

    Retrieve a specific numeric review made by a user for a given content # noqa: E501

    :param content_id: The ID of the content to retrieve the review for
    :type content_id: int
    :param user_id: The ID of the user whose review to retrieve
    :type user_id: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def get_numeric_reviews_by_user(user_id):  # noqa: E501
    """Get reviews by user

    Retrieve all numeric reviews made by a specific user # noqa: E501

    :param user_id: The ID of the user whose reviews to retrieve
    :type user_id: int

    :rtype: InlineResponse2004
    """
    return 'do some magic!'


def get_numeric_reviews_for_content(content_id):  # noqa: E501
    """Get numeric reviews for specific content

    Retrieve all numeric reviews (user ID and rating) made for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve reviews for
    :type content_id: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def get_recommendations_for_user(user_id, profile_id):  # noqa: E501
    """Get recommendations for a profile

    Retrieve content recommendations based on a user&#x27;s viewing history # noqa: E501

    :param user_id: The ID of the user to retrieve recommendations for
    :type user_id: int
    :param profile_id: The ID of the profile to retrieve recommendations for
    :type profile_id: int

    :rtype: InlineResponse2006
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
    return InlineResponse2006.from_dict({"recommendations": recommendations}), 200


def update_specific_review_for_content_by_user(body, content_id, user_id):  # noqa: E501
    """Update a specific review for content by user

    Update an existing numeric review for a given content and user # noqa: E501

    :param body: The updated review data
    :type body: dict | bytes
    :param content_id: The ID of the content to update the review for
    :type content_id: int
    :param user_id: The ID of the user whose review is being updated
    :type user_id: int

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        body = UsersUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_content_views(content_id):  # noqa: E501
    """Get number of views for content

    Retrieve the number of views for a specific content # noqa: E501

    :param content_id: The ID of the content to retrieve views for
    :type content_id: int

    :rtype: InlineResponse200
    """
    result = fetch_view_count(content_id)
    if result['status'] == 'success':
        views = result['data'][0]['view_count'] if result['data'] else 0
        return {'views': views}, 200
    else:
        return {'error': result['error']}, 400


def add_content_view(content_id, body):
    """
    Maneja la solicitud POST para agregar una nueva entrada de 'views'.

    Agrega una nueva entrada de 'views' asociada a un contenido específico.

    :param content_id: El ID del contenido para el cual agregar la entrada de 'views'.
    :type content_id: int
    :param body: El cuerpo de la solicitud que contiene los datos necesarios para agregar la entrada de 'views'.
    :type body: dict
    :rtype: dict, int
    :return: Devuelve un mensaje indicando si la operación fue exitosa o si ocurrió un error.
    """
    view_count = body.get('view_count')

    result = add_view(content_id, view_count)
    if result['status'] == 'success':
        return {'message': 'View added successfully'}, 201
    else:
        return {'error': result['error']}, 400


def update_content_view(content_id, body):
    """
    Maneja la solicitud PUT para actualizar la cantidad de 'views'.

    Actualiza la cantidad de 'views' asociada a un contenido específico.

    :param content_id: El ID del contenido para actualizar la cantidad de 'views'.
    :type content_id: int
    :param body: El cuerpo de la solicitud que contiene la nueva cantidad de 'views'.
    :type body: dict
    :rtype: dict, int
    :return: Devuelve un mensaje indicando si la operación de actualización fue exitosa, si no se encontró ningún registro para actualizar, o si ocurrió un error.
    """
    new_view_count = body.get('new_view_count')
    result = update_view(content_id, new_view_count)
    if result['status'] == 'success' and result['rowcount'] > 0:
        return {'message': 'View count updated successfully'}, 200
    elif result['status'] == 'success':
        return {'message': 'No record found to update'}, 404
    else:
        return {'error': result['error']}, 400

def delete_content_view(content_id):
    """
    Maneja la solicitud DELETE para eliminar una entrada de 'views'.

    Elimina una entrada de 'views' asociada a un contenido específico.

    :param content_id: El ID del contenido para el cual eliminar la entrada de 'views'.
    :type content_id: int
    :rtype: dict, int
    :return: Devuelve un mensaje indicando si la operación de eliminación fue exitosa, si no se encontró ningún registro para eliminar, o si ocurrió un error.
    """
    result = delete_view(int(content_id))
    if result['status'] == 'success' and result['rowcount'] > 0:
        return {'message': 'View deleted successfully'}, 200
    elif result['status'] == 'success':
        return {'message': 'No record found to delete'}, 404
    else:
        return {'error': result['error']}, 400

def get_continue_watching(user_id, profile_id, content_id):
    """
    Recupera el último minuto visto de un contenido específico.
    """
    result = fetch_continue_watching(user_id, profile_id, content_id)
    if result['status'] == 'success' and result['data']:
        return {'last_watched_minute': result['data'][0]['last_watched_minute']}, 200
    elif result['status'] == 'success':
        return {'message': 'No record found'}, 404
    else:
        return {'error': result['error']}, 400

def add_continue_watching(user_id, profile_id, content_id, body):
    """
    Agrega una nueva entrada de 'continuar viendo' para un contenido específico.
    """
    last_watched_minute = body.get('last_watched_minute')
    result = insert_continue_watching(user_id, profile_id, content_id, last_watched_minute)
    if result['status'] == 'success':
        return {'message': 'Continue watching entry created successfully'}, 201
    else:
        return {'error': result['error']}, 400

def update_continue_watching(user_id, profile_id, content_id, body):
    """
    Actualiza el último minuto visto de un contenido específico.
    """
    new_last_watched_minute = body.get('new_last_watched_minute')
    result = update_continue_entry(user_id, profile_id, content_id, new_last_watched_minute)
    if result['status'] == 'success' and result['rowcount'] > 0:
        return {'message': 'Continue watching entry updated successfully'}, 200
    elif result['status'] == 'success':
        return {'message': 'No record found to update'}, 404
    else:
        return {'error': result['error']}, 400

def delete_continue_watching(user_id, profile_id, content_id):
    """
    Elimina una entrada de 'continuar viendo' para un contenido específico.
    """
    result = delete_continue_entry(user_id, profile_id, content_id)
    if result['status'] == 'success' and result['rowcount'] > 0:
        return {'message': 'Continue watching entry deleted successfully'}, 200
    elif result['status'] == 'success':
        return {'message': 'No record found to delete'}, 404
    else:
        return {'error': result['error']}, 400
